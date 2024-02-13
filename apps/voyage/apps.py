from django.conf import settings
from django.apps import AppConfig


class VoyageConfig(AppConfig):
    name = "apps.voyage"
    verbose_name = "Voyage"

    def ready(self):
        # pylint: disable=unused-import
        # pylint: disable=import-outside-toplevel
        from . import signals

        if settings.DEBUG:
            print("Loaded aperture signals")

