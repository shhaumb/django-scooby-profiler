from django.conf import settings


SCOOBY_DEBUG = getattr(settings, 'SCOOBY_DEBUG', settings.DEBUG)
SCOOBY_BACKEND = getattr(settings, 'SCOOBY_BACKEND',
                         'scooby.backends.RedisBackend')
SCOOBY_REDIS_BACKEND_CONFIG = getattr(settings, 'SCOOBY_REDIS_BACKEND_CONFIG',
                                      None)
SCOOBY_SECRET_KEY = settings.SCOOBY_SECRET_KEY
SCOOBY_COOKIE_NAME = 'scoobydoobydoo'
