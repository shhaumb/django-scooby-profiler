import datetime

from scooby.plugins_base import Plugin


class ProcessTimePluginData(object):
    def __init__(self):
        self.start = None
        self.end = None

    def as_json_dict(self):
        process_time = None
        if self.start and self.end:
            process_time = int((self.end - self.start).total_seconds() * 1000)
        return {
            'start': self.start and self.start.isoformat(),
            'end': self.end and self.end.isoformat(),
            'process_time': process_time,
        }


class ProcessTimePlugin(Plugin):
    Data = ProcessTimePluginData

    def __init__(self):
        super(ProcessTimePlugin, self).__init__(name='ProcessTime')

    def on_process_request(self, plugin_data, *args, **kwargs):
        plugin_data.start = datetime.datetime.now()

    def on_process_response(self, plugin_data, *args, **kwargs):
        plugin_data.end = datetime.datetime.now()
