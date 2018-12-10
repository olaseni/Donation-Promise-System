from django.apps import AppConfig


class DpsMainConfig(AppConfig):
    name = 'dps_main'
    verbose_name = 'Donation Promise System'

    def ready(self):
        """
        Hook for loading signals
        """
        super().ready()
        from . import signals
        signals.initialize()
