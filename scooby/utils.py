import os
import sys
import redis
import inspect

from django.conf import settings
from django.db.models import Model


def get_redis():
    return redis.StrictRedis(**settings.SCOOBY_REDIS_CONFIG)


def curate_filename(filename):
    for path in reversed(sys.path):
        if ('dist-packages' in path or 'site-packages' in path):
            continue
        if path and filename.startswith(path):
            filename = filename.split(path, 1)[1]
            if filename.startswith(os.path.sep):
                filename = filename[1:]
            break
    return filename
    

def get_repr(value):
    if isinstance(value, (
            int, float, bool, str, list, tuple, dict, Model)):
        return repr(value)
    else:
        return "<%s>" % (value.__class__.__name__)

def get_stack():
    frame_infos = inspect.stack(9)
    stack = []
    for frame_info in frame_infos[2:]:
        frame_locals = inspect.getargvalues(frame_info.frame).locals
        local_vars = {}
        if not ('dist-packages' in frame_info.filename or
                'site-packages' in frame_info.filename):
            for var in frame_locals:
                value = get_repr(frame_locals[var])
                local_vars[var] = value
        del frame_locals
        stack.append({
            'filename': curate_filename(frame_info.filename),
            'lineno': frame_info.lineno,
            'function': frame_info.function,
            'code_context': frame_info.code_context,
            'line_index': frame_info.index,
            'local_vars': local_vars,
        })
    del frame_infos
    return stack
