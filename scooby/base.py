import json

from .plugins_finder import get_plugins


class ScoobyData(object):
    def __init__(self, profiler=None):
        self.profiler = profiler
        self.plugins = get_plugins()
        self.plugins_data = {}
        for plugin in self.plugins:
            self.plugins_data[plugin.name] = plugin.Data()

    def on_process_request(self, request):
        for plugin in self.plugins:
            if hasattr(plugin, 'on_process_request'):
                plugin_data = self.plugins_data[plugin.name]
                plugin.on_process_request(
                    plugin_data, request)

    def on_process_view(self, request, view, view_args, view_kwargs):
        for plugin in self.plugins:
            if hasattr(plugin, 'on_process_view'):
                plugin_data = self.plugins_data[plugin.name]
                plugin.on_process_view(
                    plugin_data, request,
                    view, view_args, view_kwargs)

    def on_process_response(self, request, response):
        for plugin in self.plugins:
            if hasattr(plugin, 'on_process_response'):
                plugin_data = self.plugins_data[plugin.name]
                plugin.on_process_response(
                    plugin_data, request, response)

    def as_json(self):
        plugins_data_json = {}
        for plugin_name in self.plugins_data:
            plugin_data = self.plugins_data[plugin_name]
            plugins_data_json[plugin_name] = plugin_data.as_json_dict()
        return json.dumps({
            'plugins_data': plugins_data_json
        })
