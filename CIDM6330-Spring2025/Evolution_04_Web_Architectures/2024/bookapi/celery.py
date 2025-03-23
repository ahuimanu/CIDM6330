# django_celery/celery.py

import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookapi.settings")

app = Celery("bookapi")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'

# Below is for illustration purposes. We
# configured so we can adjust scheduling
# in the Django admin to manage all
# Periodic Tasks like below
app.conf.beat_schedule = {
    "multiply-task-crontab": {
        "task": "multiply_two_numbers",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
        "args": (16, 16),
    },
    "multiply-every-5-seconds": {
        "task": "multiply_two_numbers",
        "schedule": 5.0,
        "args": (16, 16),
    },
    "add-every-30-seconds": {
        "task": "movies.tasks.add",
        "schedule": 30.0,
        "args": (16, 16),
    },
}
