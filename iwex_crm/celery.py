import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue

from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iwex_crm.settings')

app = Celery('iwex_crm')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# set celery timezone
app.conf.timezone = settings.TIME_ZONE


app.conf.beat_schedule = {
    'reset_documents_serial_numbers': {
        'task': 'applications.common.tasks.reset_documents_serial_numbers',
        'schedule': crontab(hour=0, minute=0),  # Every day at 00:00 AM
    },
    # 'test_reset_documents_serial_numbers': {
    #     'task': 'applications.common.tasks.reset_documents_serial_numbers',
    #     'schedule': crontab(minute='*/5'),  # Every 5 minutes
    # }
}

app.conf.task_default_queue = 'default'

app.conf.task_queues = (
    Queue('default', routing_key='default'),
    Queue('beats', routing_key='beats'),
)

app.conf.update(
    task_routes={
        'applications.common.tasks.reset_documents_serial_numbers': {'queue': 'beats'},
        '*': {'queue': 'default'},
    })
