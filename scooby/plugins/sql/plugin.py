import threading
from datetime import datetime

from django.db.models.sql.compiler import SQLCompiler

from scooby.plugins_base import Plugin


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
        time_taken = int((datetime.now() - start).total_seconds() * 1000.0)
        threadlocal.sql_plugin_data.insert(
            query=q,
            start=start,
            time_taken=time_taken,
            using=self.using)


class SQLPluginData(object):
    def __init__(self):
        self.queries = []

    def insert(self, query, start, time_taken, using):
        self.queries.append({
            'query': query,
            'start': start.isoformat(),
            'time_taken': time_taken,
            'using': using,
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
