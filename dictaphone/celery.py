import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictaphone.settings')

app = Celery('dictaphone')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()