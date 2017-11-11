import threading

from scooby.plugins_base import Plugin
from scooby.utils import get_stack


threadlocal = threading.local()

def init_threadlocal(threadlocal):
    threadlocal.initialized = True
    threadlocal.log_plugin_data = None

init_threadlocal(threadlocal)


class CustomLogPluginData(object):
    def __init__(self):
        self.logs = []

    def log(self, s, stack):
        self.logs.append({
            's': s,
            'stack': stack,
        })

    def as_json_dict(self):
        return {
            'logs': self.logs,
        }


def log(*args):
    s = ' '.join([(arg if isinstance(arg, str) else repr(arg))
                  for arg in args])
    if not hasattr(threadlocal, 'initialized'):
        return
    if threadlocal.log_plugin_data:
        stack = get_stack()
        threadlocal.log_plugin_data.log(s, stack)


class CustomLogPlugin(Plugin):
    Data = CustomLogPluginData

    def __init__(self):
        super(CustomLogPlugin, self).__init__(name='CustomLog')

    def on_process_request(self, log_plugin_data, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.log_plugin_data = log_plugin_data

    def on_process_response(self, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.log_plugin_data = None
