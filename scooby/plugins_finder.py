from .plugins.viewname import ViewNamePlugin
from .plugins.sql import SQLPlugin
from .plugins.processtime import ProcessTimePlugin
from .plugins.customlog import CustomLogPlugin

plugin_instances = [
    ViewNamePlugin(),
    ProcessTimePlugin(),
    SQLPlugin(),
    CustomLogPlugin(),
]

def get_plugins():
    return plugin_instances
