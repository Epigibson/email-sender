@echo off
echo Starting Celery worker...
celery -A celery_worker worker --loglevel=info --pool=solo

:: To start the beat scheduler in a separate window, uncomment the following lines:
:: start "Celery Beat" cmd /k "cd /d %~dp0 && celery -A celery_worker beat --loglevel=info"
