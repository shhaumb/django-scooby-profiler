from django.apps import AppConfig

from .plugins_finder import get_plugins


class ScoobyAppConfig(AppConfig):
    name = 'scooby'
    verbose_name = 'Scooby'

    def ready(self):
        plugins = get_plugins()
        for plugin in plugins:
            if not plugin.is_instrumented():
                plugin.instrument()
