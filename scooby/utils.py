import os
import sys
import inspect
import importlib

from django.db.models import Model

from . import settings


global_backend = None
def get_backend():
    global global_backend
    if global_backend is None:
        backend_module_path, backend_class_name = settings.SCOOBY_BACKEND.rsplit('.', 1)
        backend_module = importlib.import_module(backend_module_path)
        backend_class = getattr(backend_module, backend_class_name)
        global_backend = backend_class()
    return global_backend

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


def get_repr(value, nest_level=0):
    try:
        unicode_cls = unicode
    except NameError:
        # Python3
        unicode_cls = str
    if type(value).__name__ == 'SimpleLazyObject':
        return '<SimpleLazyObject>'
    elif isinstance(value, (
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
    elif nest_level == 0 and isinstance(value, (tuple, list, dict)):
        if isinstance(value, tuple):
            return "(%s)" % (', '.join(
                [get_repr(item, nest_level+1) for item in value]))
        elif isinstance(value, list):
            return "[%s]" % (', '.join(
                [get_repr(item, nest_level+1) for item in value]))
        elif isinstance(value, dict):
            return "{%s}" % (', '.join([
                '%s: %s' % (get_repr(key), get_repr(value, nest_level+1))
                for (key, value) in value.items()]))
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
