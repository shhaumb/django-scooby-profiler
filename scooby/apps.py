from django.apps import AppConfig

from .plugins_finder import get_plugins
from . import settings


class ScoobyAppConfig(AppConfig):
    name = 'scooby'
    verbose_name = 'Scooby'

    def ready(self):
        if not settings.SCOOBY_DEBUG:
            return
        plugins = get_plugins()
        for plugin in plugins:
            if not plugin.is_instrumented():
                plugin.instrument()
