from django.conf import settings

import redis


def get_redis():
  return redis.StrictRedis(**settings.SCOOBY_REDIS_CONFIG) 
