import redis
import threading


class RedisQueue(object):
    def __init__(self, **redis_args):
        self.redis = redis.Redis(**redis_args, decode_responses=True)

    def put(self, queue: str, message):
        if not queue:
            raise ValueError("'queue' argument cannot be None/empty")
        if not message:
            raise ValueError("'message' argument cannot be None/empty")

        self.redis.rpush(f"pyredq:{queue}", message)

    def subscribe(self, queue: str, callback, background: bool = False):
        if not queue:
            raise ValueError("'queue' argument cannot be None/empty")
        if not callback:
            raise ValueError("'callback' function argument cannot be None")

        if background:
            t = threading.Thread(target=self._blocking_pop, args=(queue, callback))
            t.setDaemon(True)
            t.start()
        else:
            self._blocking_pop(queue, callback)

    def _blocking_pop(self, queue: str, callback):
        print(f"pyredq -- Subscribed to messages on '{queue}'", flush=True)
        while True:
            _, msg = self.redis.blpop(f"pyredq:{queue}")
            if msg:
                callback(msg)
