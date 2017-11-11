from scooby.plugins_base import Plugin


class ViewNamePluginData(object):
    def __init__(self):
        self.view_name = None
        self.args = ()
        self.kwargs = {}

    def as_json_dict(self):
        return {
            'view_name': self.view_name,
            'args': self.args,
            'kwargs': self.kwargs,
        }


class ViewNamePlugin(Plugin):
    Data = ViewNamePluginData

    def __init__(self):
        super(ViewNamePlugin, self).__init__(name='ViewName')

    def on_process_view(self, plugin_data, request,
            view, view_args, view_kwargs):
        plugin_data.view_name = '%s.%s' % (view.__module__, view.__name__)
        plugin_data.args = view_args
        plugin_data.kwargs = view_kwargs
