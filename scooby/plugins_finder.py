from .plugins.viewname import ViewNamePlugin
from .plugins.sql import SQLPlugin
from .plugins.processtime import ProcessTimePlugin
from .plugins.customlog import CustomLogPlugin
from .plugins.memcache import MemcachePlugin
from .plugins.thriftpy import ThriftpyPlugin

plugin_instances = [
    ViewNamePlugin(),
    ProcessTimePlugin(),
    SQLPlugin(),
    CustomLogPlugin(),
    MemcachePlugin(),
    ThriftpyPlugin(),
]

plugins_to_be_used = [p for p in plugin_instances if p.should_be_used()]

def get_plugins():
    return plugins_to_be_used
