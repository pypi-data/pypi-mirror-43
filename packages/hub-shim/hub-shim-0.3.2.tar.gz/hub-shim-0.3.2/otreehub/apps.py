from django.apps import AppConfig



class OTreeHubConfig(AppConfig):
    name = 'otreehub'

    def ready(self):
        from . import signals
