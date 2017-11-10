from scooby.plugins_base import Plugin


class ViewNamePluginData(object):
    def __init__(self):
        self.view_name = None

    def as_json_dict(self):
        return {
            'view_name': self.view_name,
        }


class ViewNamePlugin(Plugin):
    Data = ViewNamePluginData

    def __init__(self):
        super(ViewNamePlugin, self).__init__(name='ViewName')

    def on_process_view(self, plugin_data, request, view, *args):
        plugin_data.view_name = '%s.%s' % (view.__module__, view.__name__)
