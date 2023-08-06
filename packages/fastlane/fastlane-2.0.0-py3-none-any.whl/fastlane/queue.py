# Standard Library
from datetime import datetime, timezone
from uuid import uuid4

# 3rd Party
from flask import current_app
from redis.client import Pipeline

# Fastlane
from fastlane.models.categories import Categories
from fastlane.utils import dumps, get_next_cron_timestamp, loads, parse_time, to_unix
from fastlane.worker.job import monitor_job, run_job, send_email, send_webhook


def _enqueue_message(redis, logger, msg, message_key, message_hash_key, queue_name):
    timestamp = to_unix(datetime.utcnow())
    pipe = redis.pipeline()
    pipe.set(message_key, msg.serialize())
    pipe.zadd(message_hash_key, {msg.id: timestamp})
    pipe.lpush(queue_name, msg.id)

    if msg.cron_str is not None:
        next_dt = get_next_cron_timestamp(msg.cron_str)
        timestamp = to_unix(next_dt)

        _enqueue_at_timestamp(
            pipe,
            logger,
            msg.queue,
            Queue.get_message_name,
            timestamp,
            msg.category,
            msg.cron_str,
            *msg.args,
            **msg.kwargs,
        )

    return pipe.execute()


def _enqueue_at_timestamp(
    redis,
    logger,
    queue_name,
    message_key_fn,
    timestamp,
    category,
    cron_str,
    *args,
    **kw,
):
    execute_now = False

    if not isinstance(redis, Pipeline):
        execute_now = True
        redis = redis.pipeline()

    msg = Message(queue_name, category, cron_str, *args, **kw)

    logger.info(
        "Scheduling message to run at future time.",
        operation="schedule",
        timestamp=timestamp,
        category=category,
    )
    redis.set(message_key_fn(msg.id), msg.serialize())
    redis.zadd(Queue.SCHEDULED_QUEUE_NAME, {msg.id: timestamp})

    if execute_now:
        redis.execute()

    return msg.id


def _dequeue(redis, queue_names, blocking=False, timeout=1):
    queue = ""

    if isinstance(queue_names, (tuple, list)) or blocking:
        result = redis.blpop(queue_names, timeout=max(timeout, 1))

        if result is None:
            return None

        queue, item = result
    else:
        item = redis.lpop(queue_names)
        queue = queue_names[0]

    if item is None:
        return None

    queue_hash_name = f"{Queue.QUEUE_HASH_NAME}:{queue}"
    msg_id = item.decode("utf-8")

    pipe = redis.pipeline()
    key = Queue.get_message_name(msg_id)
    pipe.zrem(queue_hash_name, msg_id)
    pipe.get(key)
    pipe.delete(key)
    _, message_data, _ = pipe.execute()

    return Message.deserialize(message_data.decode("utf-8"))


class Message:
    def __init__(self, queue, category, cron_str, *args, **kw):
        self.queue = queue
        self.category = category
        self.cron_str = cron_str

        if "id" in kw:
            self.id = kw.pop("id")  # pylint: disable=invalid-name
        else:
            self.id = str(uuid4())

        self.args = args
        self.kwargs = kw

    def serialize(self):
        return dumps(self)

    @classmethod
    def deserialize(cls, data):
        instance = Message("", "", None)
        instance.__dict__ = loads(  # pylint: disable=attribute-defined-outside-init
            data
        )

        return instance

    def run(self):
        if self.category == Categories.Job:
            current_app.logger.debug("Running job...")
            run_job(*self.args, **self.kwargs)

        if self.category == Categories.Monitor:
            current_app.logger.debug("Running Monitoring...")
            monitor_job(*self.args, **self.kwargs)

        if self.category == Categories.Webhook:
            current_app.logger.debug("Running Webhook...")
            send_webhook(*self.args, **self.kwargs)

        if self.category == Categories.Notify:
            current_app.logger.debug("Running Notification...")
            send_email(*self.args, **self.kwargs)


class QueueGroup:
    def __init__(self, logger, redis, queues):
        self.logger = logger
        self.queues = queues
        self.redis = redis

    def dequeue(self, queues=None, timeout=1):
        queues_to_pop = []

        if queues is None:
            queues_to_pop = [q.queue_name for q in self.queues]
        else:
            queues_to_pop = [q.queue_name for q in self.queues if q.queue_id in queues]

        return _dequeue(self.redis, queues_to_pop, blocking=True, timeout=timeout)

    def move_jobs(self):
        logger = self.logger.bind(operation="move_jobs")

        lock = self.redis.lock(
            Queue.MOVE_JOBS_LOCK_NAME,
            timeout=5,
            sleep=0.1,
            blocking_timeout=500,
            thread_local=False,
        )

        if not lock.acquire():
            logger.info("Lock could not be acquired. Trying to move jobs again later.")

            return None

        moved_items = []

        try:
            timestamp = to_unix(datetime.utcnow())

            pipe = self.redis.pipeline()
            pipe.zrangebyscore(Queue.SCHEDULED_QUEUE_NAME, "-inf", timestamp)
            pipe.zremrangebyscore(Queue.SCHEDULED_QUEUE_NAME, "-inf", timestamp)
            items, _ = pipe.execute()

            if not items:
                logger.info("No jobs in need of moving right now.")

                return moved_items

            logger.info("Found jobs in need of moving.", job_count=len(items))

            for message_id in items:
                key = Queue.get_message_name(message_id.decode("utf-8"))
                data = self.redis.get(key)
                msg = Message.deserialize(data.decode("utf-8"))
                logger.info(
                    "Moving job to queue.",
                    queue_name=msg.queue,
                    job_id=msg.id,
                    msg=msg.serialize(),
                )
                queue_hash_name = f"{Queue.QUEUE_HASH_NAME}:{msg.queue}"
                _enqueue_message(
                    self.redis, self.logger, msg, key, queue_hash_name, msg.queue
                )
                moved_items.append(msg)

            logger.info("Moved jobs successfully.")

            return moved_items
        finally:
            lock.release()


class Queue:
    QUEUE_NAME = "fastlane:message-queue"
    QUEUE_HASH_NAME = "fastlane:message-queue-ids"
    SCHEDULED_QUEUE_NAME = "fastlane:scheduled-messages:items"
    MOVE_JOBS_LOCK_NAME = "fastlane:move-jobs-lock"
    MESSAGE_DETAILS_NAME = "fastlane:scheduled-message"

    def __init__(self, logger, redis, queue_name="main"):
        self.redis = redis
        self.queue_id = queue_name
        self.queue_name = f"{Queue.QUEUE_NAME}:{queue_name}"
        self.queue_hash_name = f"{Queue.QUEUE_HASH_NAME}:{queue_name}"
        self.logger = logger.bind(queue_id=self.queue_id, queue_name=self.queue_name)

    def enqueue(self, category, *args, **kw):
        msg = Message(self.queue_name, category, None, *args, **kw)

        self.logger.info(
            "Sending message to queue.", operation="enqueue", category=category
        )

        return self.__enqueue(msg)

    def __enqueue(self, msg):
        _enqueue_message(
            self.redis,
            self.logger,
            msg,
            self.get_message_name(msg.id),
            self.queue_hash_name,
            self.queue_name,
        )

        return msg.id

    @classmethod
    def get_message_name(cls, message_id):
        return f"{Queue.MESSAGE_DETAILS_NAME}:{message_id}"

    def enqueue_at(self, timestamp, category, *args, **kw):
        return self.__enqueue_at_timestamp(timestamp, category, None, *args, **kw)

    def enqueue_in(self, incr, category, *args, **kw):
        start_in = parse_time(incr)
        future_date = datetime.now(tz=timezone.utc) + start_in
        timestamp = to_unix(future_date)

        return self.__enqueue_at_timestamp(timestamp, category, None, *args, **kw)

    def enqueue_cron(self, cron, category, *args, **kw):
        next_dt = get_next_cron_timestamp(cron)
        timestamp = to_unix(next_dt)

        return self.__enqueue_at_timestamp(timestamp, category, cron, *args, **kw)

    def __enqueue_at_timestamp(self, timestamp, category, cron_str, *args, **kw):
        if not isinstance(timestamp, (int,)):
            raise RuntimeError(
                f"timestamp must be a UTC Unix Timestamp (integer), not {type(timestamp)}"
            )

        return _enqueue_at_timestamp(
            self.redis,
            self.logger,
            self.queue_name,
            self.get_message_name,
            timestamp,
            category,
            cron_str,
            *args,
            **kw,
        )

    def dequeue(self, blocking=False, timeout=1):
        return _dequeue(self.redis, self.queue_name, blocking=blocking, timeout=timeout)

    def is_scheduled(self, message_id):
        return self.redis.zrank(Queue.SCHEDULED_QUEUE_NAME, message_id) is not None

    def is_enqueued(self, message_id):
        return self.redis.zrank(self.queue_hash_name, message_id) is not None

    def deschedule(self, message_id):
        logger = self.logger.bind(operation="deschedule", message_id=message_id)
        logger.info("Descheduling job from queue.")
        pipe = self.redis.pipeline()
        pipe.zrem(Queue.SCHEDULED_QUEUE_NAME, message_id)
        pipe.delete(self.get_message_name(message_id))
        results = pipe.execute()

        if results[0] == 1:
            logger.info("Descheduling job successful.")
        else:
            logger.info("Descheduling job failed (maybe job was not found).")

        return results[0] == 1
