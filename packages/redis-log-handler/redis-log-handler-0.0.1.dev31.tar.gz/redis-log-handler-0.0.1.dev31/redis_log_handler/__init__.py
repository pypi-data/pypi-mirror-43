import logging
from typing import Any

from redis import StrictRedis


class RedisBaseHandler(logging.StreamHandler):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.redis_client = StrictRedis(**kwargs)

    def emit(self, message: logging.LogRecord):
        raise NotImplementedError("Emit functionality from base class not overridden.")


class RedisChannelHandler(RedisBaseHandler):
    def __init__(self, channel: str, **kwargs: Any):
        super().__init__(**kwargs)

        self.channel = channel

    def emit(self, message: logging.LogRecord):
        self.redis_client.publish(self.channel, str(message))


class RedisKeyHandler(RedisBaseHandler):
    def __init__(self, key: str, ttl: int = None, **kwargs):
        super().__init__(**kwargs)

        self.key = key
        self.ttl = ttl

        if self.ttl:
            self.redis_client.expire(self.key, self.ttl)

    def emit(self, message: logging.LogRecord):
        self.redis_client.rpush(self.key, str(message))
