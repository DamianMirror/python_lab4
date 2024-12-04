from django.apps import AppConfig


class UniversityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'university'

    def ready(self):
        #Import your Dash apps here to ensure they are registered
        pass
