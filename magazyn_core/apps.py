from django.apps import AppConfig


class MagazynCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'magazyn_core'

    def ready(self):
        import magazyn_core.signals

    
