from django.conf import settings


SCOOBY_DEBUG = getattr(settings, 'SCOOBY_DEBUG', settings.DEBUG)
SCOOBY_REDIS_CONFIG = settings.SCOOBY_REDIS_CONFIG
SCOOBY_SECRET_KEY = settings.SCOOBY_SECRET_KEY
SCOOBY_COOKIE_NAME = 'scoobydoobydoo'
