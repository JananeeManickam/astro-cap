import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astrocap_app.settings')

app = Celery('astrocap_app')

# Use Django settings for Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Set up periodic tasks
app.conf.beat_schedule = {
    'fetch-hubble-data-every-15-minutes': {
        'task': 'pictures.tasks.fetch_hubble_telescope_data',
        'schedule': 15 * 60,  # 15 minutes in seconds
    },
}