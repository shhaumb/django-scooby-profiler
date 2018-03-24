import threading
from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler

from scooby.plugins_base import Plugin
from scooby.utils import get_stack


def escaped_string(s):
    return "'%s'" % (
        s.replace('\\', '\\\\').replace("'", "''")
    )

def get_escaped_params(params):
    escaped_params = []
    for param in params:
        if isinstance(param, str):
            escaped_params.append(escaped_string(param))
        elif isinstance(param, bytes):
            escaped_params.append(escaped_string(param.decode("iso-8859-1")))
        elif isinstance(param, bool):
            escaped_params.append(int(param))
        else:
            escaped_params.append(param)
    return tuple(escaped_params)


threadlocal = threading.local()

def init_threadlocal(threadlocal):
    threadlocal.initialized = True
    threadlocal.sql_plugin_data = None

init_threadlocal(threadlocal)

def execute_sql(self, *args, **kwargs):
    if not hasattr(threadlocal, 'initialized'):
        init_threadlocal(threadlocal)

    if not threadlocal.sql_plugin_data:
        return self.execute_sql_default(*args, **kwargs)

    try:
        q, params = self.as_sql()
    except:
        return self.execute_sql_default(*args, **kwargs)

    start = datetime.now()
    try:
        return self.execute_sql_default(*args, **kwargs)
    finally:
        end = datetime.now()
        time_taken = (end - start).total_seconds() * 1000.0
        threadlocal.sql_plugin_data.insert(
            query=q,
            params=params,
            start=start,
            end=end,
            time_taken=time_taken,
            using=self.using,
            stack=get_stack()
        )


class SQLPluginData(object):
    def __init__(self):
        self.queries = []

    def insert(self, query, params, start, end, time_taken, using, stack):
        params = get_escaped_params(params)
        self.queries.append({
            'query_template': query,
            'params': params,
            'query': (query % params),
            'start': start.isoformat(),
            'end': end.isoformat(),
            'time_taken': time_taken,
            'using': using,
            'stack': stack,
        })

    def as_json_dict(self):
        return {
            'queries': self.queries,
        }


class SQLPlugin(Plugin):
    Data = SQLPluginData

    def __init__(self):
        super(SQLPlugin, self).__init__(name='SQL')

    def instrument(self):
        SQLCompiler.execute_sql_default = SQLCompiler.execute_sql
        SQLCompiler.execute_sql = execute_sql
        super(SQLPlugin, self).instrument()

    def on_process_request(self, sql_plugin_data, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.sql_plugin_data = sql_plugin_data

    def on_process_response(self, *args, **kwargs):
        init_threadlocal(threadlocal)
        threadlocal.sql_plugin_data = None
