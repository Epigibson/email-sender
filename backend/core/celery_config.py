from datetime import timedelta
from celery.schedules import crontab
from core.config import settings

# Broker settings
broker_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
result_backend = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

# Task settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

# Beat settings (for scheduled tasks)
beat_schedule = {
    'send-scheduled-emails': {
        'task': 'services.email_services.EmailService.send_scheduled_emails',
        'schedule': 60.0,  # Check every minute
    },
}

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 100
task_acks_late = True
task_reject_on_worker_lost = True
