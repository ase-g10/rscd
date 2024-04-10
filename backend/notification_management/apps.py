# your_app_name/apps.py
from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    name = 'notification_management'

    def ready(self):
        import notification_management.signals
