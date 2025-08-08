import os
from celery import Celery
from core.config import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')

app = Celery('email_scheduler')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('core.config.settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    # Executes every 10 minutes
    'send-scheduled-emails-every-10-minutes': {
        'task': 'services.email_services.send_scheduled_emails',
        'schedule': 600.0,  # 10 minutes in seconds
    },
}

if __name__ == '__main__':
    app.start()
