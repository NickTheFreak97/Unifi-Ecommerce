import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Unifi_Ecommerce.settings")

app = Celery("Unifi_Ecommerce")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()