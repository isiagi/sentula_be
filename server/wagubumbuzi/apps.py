from django.apps import AppConfig


class WagubumbuziConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagubumbuzi'

    def ready(self):
        # Import signals when the app is ready
        import wagubumbuzi.signals  # Replace with your actual app name