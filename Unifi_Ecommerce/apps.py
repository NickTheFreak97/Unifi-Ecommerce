from django.apps import AppConfig
import os

class UnifiEcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Unifi_Ecommerce'

    def ready(self):
        from users.models.user.user import User

        try:
            if not User.objects.filter(username=os.environ.get('DJANGO_ADMIN_USERNAME')).exists():
                User.objects.create_superuser(
                    username=os.environ.get('DJANGO_ADMIN_USERNAME'),
                    email=os.environ.get('DJANGO_ADMIN_EMAIL'),
                    password=os.environ.get('DJANGO_ADMIN_PASSWORD')
                )
        except Exception:
             # In case this runs alongside a migration, when User table doesn't exist yet.
             pass