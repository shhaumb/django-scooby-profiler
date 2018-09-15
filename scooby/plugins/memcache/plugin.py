import pickle
import threading
import datetime
import functools

from scooby.plugins_base import Plugin
from scooby.utils import get_stack


threadlocal = threading.local()

def init_threadlocal(threadlocal):
    threadlocal.initialized = True
    threadlocal.memcache_plugin_data = None

init_threadlocal(threadlocal)


class MemcachePluginData(object):
    def __init__(self):
        self.queries = []

    def insert(self, func_name, arg, start, end, time_taken, stack):
        self.queries.append({
            'func_name': func_name,
            'arg': arg,
            'start': start.isoformat(),
            'end': end.isoformat(),
            'time_taken': time_taken,
            'stack': stack,
        })

    def as_json_dict(self):
        return {
            'queries': self.queries,
        }

def record(func):
    @functools.wraps(func)
    def wrapped_method(self, *args, **kwargs):
        if not hasattr(threadlocal, 'initialized'):
            init_threadlocal(threadlocal)

        if not threadlocal.memcache_plugin_data:
            return func(self, *args, **kwargs)

        func_name = func.__name__
        arg = None
        if len(args) > 0:
            arg = args[0]
            if isinstance(arg, dict):
                arg = list(arg.keys())
        start = datetime.datetime.now()
        try:
            return func(self, *args, **kwargs)
        finally:
            end = datetime.datetime.now()
            time_taken = (end - start).total_seconds() * 1000.0
            threadlocal.memcache_plugin_data.insert(
                func_name=func_name,
                arg=arg,
                start=start,
                end=end,
                time_taken=time_taken,
                stack=get_stack()
            )
    return wrapped_method

def getScoobyMemcacheClient():
    import memcache as memc
    class ScoobyMemcacheClient(memc.Client):
        @record
        def flush_all(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).flush_all(*args, **kwargs)

        @record
        def delete_multi(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).delete_multi(*args, **kwargs)

        @record
        def delete(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).delete(*args, **kwargs)

        @record
        def incr(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).incr(*args, **kwargs)

        @record
        def decr(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).decr(*args, **kwargs)

        @record
        def add(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).add(*args, **kwargs)

        @record
        def append(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).append(*args, **kwargs)

        @record
        def prepend(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).prepend(*args, **kwargs)

        @record
        def replace(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).replace(*args, **kwargs)

        @record
        def set(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).set(*args, **kwargs)

        @record
        def cas(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).cas(*args, **kwargs)

        @record
        def set_multi(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).set_multi(*args, **kwargs)

        @record
        def get(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).get(*args, **kwargs)

        @record
        def gets(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).gets(*args, **kwargs)

        @record
        def get_multi(self, *args, **kwargs):
            return super(ScoobyMemcacheClient, self).get_multi(*args, **kwargs)

    return ScoobyMemcacheClient


def patchMemcachedCache(lib):
    from django.core.cache.backends import memcached
    class PatchedLibMemcachedCache(memcached.MemcachedCache):
        def __init__(self, server, params):
            memcached.BaseMemcachedCache.__init__(self, server, params,
                library=lib,
                value_not_found_exception=ValueError)
    memcached.MemcachedCache = PatchedLibMemcachedCache


def patchInitializedCaches(lib):
    from django.core.cache import caches
    cache_classes = caches.all()
    for cache_class in cache_classes:
        cache_class._lib = lib
        if hasattr(cache_class, '_client'):
            client_kwargs = dict(pickleProtocol=pickle.HIGHEST_PROTOCOL)
            client_kwargs.update(cache_class._options)
            cache_class._client = lib.Client(
                cache_class._servers, **client_kwargs)


class MemcachePlugin(Plugin):
    Data = MemcachePluginData

    def __init__(self):
        super(MemcachePlugin, self).__init__(name='Memcache')

    def should_be_used(self):
        try:
            import memcache
            return True
        except ImportError:
            return False

    def instrument(self):
        ScoobyMemcacheClient = getScoobyMemcacheClient()
        class Library(object):
            Client = ScoobyMemcacheClient
        patchMemcachedCache(Library)
        patchInitializedCaches(Library)
        super(MemcachePlugin, self).instrument()

    def on_process_request(self, memcache_plugin_data, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.memcache_plugin_data = memcache_plugin_data

    def on_process_response(self, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.memcache_plugin_data = None
