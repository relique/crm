import os

from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

app = Celery('crm')

# Using a string here means the worker will not have to pickle the
# object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
