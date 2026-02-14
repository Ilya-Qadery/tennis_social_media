"""
Celery configuration with error handling and task routing.
"""
import os

from celery import Celery
from celery.signals import setup_logging

# Set Django settings before any other imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.local")

app = Celery("varzesha")

# Configure from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# ADDED: Task routing for priority queues
app.conf.task_routes = {
    "varzesha.users.tasks.send_sms_verification_code": {"queue": "sms"},
    "varzesha.users.tasks.*": {"queue": "users"},
    "varzesha.matches.tasks.*": {"queue": "matches"},
}

# ADDED: Default queue
app.conf.task_default_queue = "default"


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    """Debug task to verify Celery is working."""
    print(f"Request: {self.request!r}")


# ADDED: Disable Celery's default logging to use Django's
@setup_logging.connect
def config_loggers(*args, **kwargs) -> None:
    from logging.config import dictConfig
    from django.conf import settings
    dictConfig(settings.LOGGING)