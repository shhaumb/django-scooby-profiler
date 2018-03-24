import threading
from datetime import datetime

from scooby.plugins_base import Plugin
from scooby.utils import get_stack


threadlocal = threading.local()

def init_threadlocal(threadlocal):
    threadlocal.initialized = True
    threadlocal.thriftpy_plugin_data = None

init_threadlocal(threadlocal)


def parse_args(args):
    parsed = []
    for v in args:
        parsed.append(repr(v))
    return parsed

def parse_kwargs(kwargs):
    parsed = {}
    for k, v in kwargs.items():
        if isinstance(v, bytes):
            v = str(v)
        parsed[k] = v
    return parsed

orig_req = None
def req(self, api, *args, **kwargs):
    if not hasattr(threadlocal, 'initialized'):
        init_threadlocal(threadlocal)

    if not threadlocal.thriftpy_plugin_data:
        return orig_req(self, api, *args, **kwargs)

    start = datetime.now()
    try:
        return orig_req(self, api, *args, **kwargs)
    finally:
        end = datetime.now()
        time_taken = (end - start).total_seconds() * 1000.0
        threadlocal.thriftpy_plugin_data.insert(
            service_name=self._service.__name__,
            func_name=api,
            args=args,
            kwargs=kwargs,
            start=start,
            end=end,
            time_taken=time_taken,
            stack=get_stack()
        )


class ThriftpyPluginData(object):
    def __init__(self):
        self.queries = []

    def insert(self, service_name, func_name, args, kwargs, start, end, time_taken, stack):
        self.queries.append({
            'service_name': service_name,
            'func_name': func_name,
            'args': parse_args(args),
            'kwargs': parse_kwargs(kwargs),
            'start': start.isoformat(),
            'end': end.isoformat(),
            'time_taken': time_taken,
            'stack': stack,
        })

    def as_json_dict(self):
        return {
            'queries': self.queries,
        }


class ThriftpyPlugin(Plugin):
    Data = ThriftpyPluginData

    def __init__(self):
        super(ThriftpyPlugin, self).__init__(name='Thriftpy')

    def should_be_used(self):
        try:
            import thriftpy
            return True
        except ImportError:
            return False

    def instrument(self):
        from thriftpy.thrift import TClient
        global orig_req
        orig_req = TClient._req
        TClient._req = req
        super(ThriftpyPlugin, self).instrument()

    def on_process_request(self, thriftpy_plugin_data, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.thriftpy_plugin_data = thriftpy_plugin_data

    def on_process_response(self, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.thriftpy_plugin_data = None
