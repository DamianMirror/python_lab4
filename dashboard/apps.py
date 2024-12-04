# dashboard/apps.py
from django.apps import AppConfig

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from .dash_apps import average_mark_per_student_per_subject
        from .dash_apps import average_mark_per_teacher
        from .dash_apps import student_count_per_group
        from .dash_apps import student_count_per_subject
        from .dash_apps import student_count_per_teacher
        from .dash_apps import average_mark_per_group
        from .dash_apps import main_dashboard
        # Додайте імпорт інших Dash-додатків
