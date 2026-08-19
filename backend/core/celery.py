import os

from celery import Celery

# Default is local. Production must set DJANGO_SETTINGS_MODULE=core.settings.production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

