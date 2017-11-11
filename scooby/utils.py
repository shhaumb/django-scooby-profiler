import os
import sys
import redis

from django.conf import settings

SCOOBY_PATHS_TO_IGNORE = getattr(settings,
    'SCOOBY_PATHS_TO_IGNORE', [])


def get_location(stack):
    stack_in_reverse = reversed(stack)
    next(stack_in_reverse)
    paths_to_ignore = [
        'site-packages',
        'dist-packages',
    ] + SCOOBY_PATHS_TO_IGNORE
    for frame in stack_in_reverse:
        to_continue = False
        for path in paths_to_ignore:
            if path in frame.filename:
                to_continue = True
                break
        if to_continue:
            continue
        break
    else:
        frame = stack[-1]
    filename = frame.filename
    for path in reversed(sys.path):
        if path and filename.startswith(path):
            filename = filename.split(path, 1)[1]
            if filename.startswith(os.path.sep):
                filename = filename[1:]
            break
    return {
        'filename': filename,
        'lineno': frame.lineno,
        'line': frame.line,
        'name': frame.name,
    }

def get_redis():
  return redis.StrictRedis(**settings.SCOOBY_REDIS_CONFIG)
