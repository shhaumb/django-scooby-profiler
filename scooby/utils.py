import os
import sys
import redis
import inspect
import __builtin__

from django.conf import settings
from django.db.models import Model


def get_redis():
    return redis.StrictRedis(**settings.SCOOBY_REDIS_CONFIG)


def curate_filename(filename):
    for path in reversed(sys.path):
        if ('dist-packages' in path or 'site-packages' in path or
            '/usr/lib/python' in path):
            continue
        if path and filename.startswith(path):
            filename = filename.split(path, 1)[1]
            if filename.startswith(os.path.sep):
                filename = filename[1:]
            break
    return filename


def get_repr(value):
    if not hasattr(__builtin__, 'unicode'):
        # Python3
        unicode_cls = str
    else:
        unicode_cls = unicode
    if isinstance(value, (
            int, float, bool, str, unicode_cls, type(None))):
        return repr(value)
    elif isinstance(value, Model):
        has_title_field = False
        try:
            value._meta.get_field('title')
            has_title_field = True
        except:
            pass
        if has_title_field:
            return "<%s: pk=%s title=%s>" % (
                value.__class__.__name__,
                get_repr(value.pk),
                get_repr(value.title),
            )
        return "<%s: pk=%s>" % (
            value.__class__.__name__,
            get_repr(value.pk),
        )
    elif isinstance(value, tuple):
        return "(%s)" % (', '.join([get_repr(item) for item in value]))
    elif isinstance(value, list):
        return "[%s]" % (', '.join([get_repr(item) for item in value]))
    elif isinstance(value, dict):
        return "{%s}" % (', '.join([
            '%s: %s' % (get_repr(key), get_repr(value)) for (key, value) in
            value.items()]))
    else:
        try:
            return "<%s>" % (value.__class__.__name__)
        except:
            return "<<Some object>>"

def get_stack():
    frame_infos = inspect.stack(9)
    stack = []
    for frame_info in frame_infos[2:]:
        frame, filename, lineno, function, code_context, index = frame_info
        frame_locals = inspect.getargvalues(frame).locals
        local_vars = {}
        if not ('dist-packages' in filename or
                'site-packages' in filename or
                '/usr/lib/python' in filename):
            for var in frame_locals:
                value = get_repr(frame_locals[var])
                local_vars[var] = value
        stack.append({
            'filename': curate_filename(filename),
            'lineno': lineno,
            'function': function,
            'code_context': code_context,
            'line_index': index,
            'local_vars': local_vars,
        })
        del frame_locals
        del frame
    del frame_infos
    return stack
