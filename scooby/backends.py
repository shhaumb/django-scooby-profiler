from . import settings


class RedisConfigNotProvided(Exception):
    pass

class RedisBackend(object):
    def __init__(self):
        import redis
        if settings.SCOOBY_REDIS_BACKEND_CONFIG is None:
            raise RedisConfigNotProvided(
                'SCOOBY_REDIS_BACKEND_CONFIG is not set in settings')
        self.redis = redis.StrictRedis(**settings.SCOOBY_REDIS_BACKEND_CONFIG)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, timeout=None):
        return self.redis.set(key, value, timeout)

    def delete(self, key):
        return self.redis.delete(key)
