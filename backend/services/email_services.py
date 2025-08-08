import os
import json
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import httpx
from fastapi import HTTPException, status
from core.config import settings
from celery import shared_task
from celery.schedules import crontab

# Configure logging
logger = logging.getLogger(__name__)

# In-memory storage for scheduled emails (you might want to use a database in production)
_scheduled_emails: Dict[str, Dict[str, Any]] = {}

class EmailService:
    @staticmethod
    @shared_task(bind=True, name="send_scheduled_emails")
    async def send_scheduled_emails(self, job_id: str = None):
        """
        Celery task to send scheduled emails.
        If job_id is provided, sends only that specific job's emails.
        Otherwise, sends all due scheduled emails.
        """
        if job_id:
            if job_id in _scheduled_emails:
                await EmailService._send_email_batch(_scheduled_emails[job_id])
        else:
            current_time = datetime.utcnow()
            for job_id, job_data in list(_scheduled_emails.items()):
                if job_data['end_time'] and job_data['end_time'] < current_time:
                    # Remove expired jobs
                    _scheduled_emails.pop(job_id, None)
                    continue
                    
                if job_data['next_run'] <= current_time:
                    try:
                        await EmailService._send_email_batch(job_data)
                        # Update next run time
                        job_data['next_run'] = current_time + timedelta(minutes=job_data['interval_minutes'])
                        _scheduled_emails[job_id] = job_data
                    except Exception as e:
                        logger.error(f"Error sending scheduled email job {job_id}: {str(e)}")

    @staticmethod
    async def _send_email_batch(job_data: Dict[str, Any]):
        """Helper method to send a batch of emails"""
        try:
            await EmailService.send_simple_message(
                to_emails=job_data['to_emails'],
                subject=job_data['subject']
            )
            logger.info(f"Successfully sent scheduled email batch with job_id: {job_data.get('job_id')}")
        except Exception as e:
            logger.error(f"Error in scheduled email job {job_data.get('job_id')}: {str(e)}")
            raise

    @staticmethod
    async def send_simple_message(to_emails: List[str], subject: str):
        try:
            response = await httpx.AsyncClient().post(
                f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
                auth=("api", settings.MAILGUN_API_KEY),
                data={
                    "from": settings.MAILGUN_FROM_EMAIL,
                    "to": to_emails,
                    "subject": subject,
			        "template": "Carta de delitos penales de ciberseguridad",
                    "h:X-Mailgun-Variables": '{"test": "test"}'
                },
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail="Error sending email via Mailgun"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error sending email: {str(e)}"
            )
            
    @classmethod
    def schedule_email_job(
        cls, 
        to_emails: List[str], 
        subject: str, 
        interval_minutes: int = 10, 
        duration_minutes: Optional[int] = None,
        job_id: Optional[str] = None
    ) -> str:
        """
        Schedule an email to be sent at regular intervals.
        
        Args:
            to_emails: List of email addresses to send to
            subject: Email subject
            interval_minutes: Interval in minutes between sends (default: 10)
            duration_minutes: How long to keep sending emails (in minutes). If None, sends indefinitely.
            job_id: Optional unique identifier for this job. If not provided, one will be generated.
            
        Returns:
            str: The job ID for the scheduled task
        """
        import uuid
        from datetime import datetime, timedelta
        
        job_id = job_id or f"email_job_{uuid.uuid4().hex[:8]}"
        current_time = datetime.utcnow()
        
        # Store the email configuration
        _scheduled_emails[job_id] = {
            'job_id': job_id,
            'to_emails': to_emails,
            'subject': subject,
            'interval_minutes': interval_minutes,
            'next_run': current_time + timedelta(minutes=interval_minutes),
            'end_time': current_time + timedelta(minutes=duration_minutes) if duration_minutes else None,
            'created_at': current_time
        }
        
        logger.info(f"Scheduled email job {job_id} to run every {interval_minutes} minutes")
        return job_id
    
    @classmethod
    def get_scheduled_jobs(cls) -> Dict[str, Dict[str, Any]]:
        """Get all scheduled email jobs"""
        return _scheduled_emails
    
    @classmethod
    def remove_scheduled_job(cls, job_id: str) -> bool:
        """
        Remove a scheduled email job
        
        Returns:
            bool: True if job was found and removed, False otherwise
        """
        if job_id in _scheduled_emails:
            _scheduled_emails.pop(job_id, None)
            logger.info(f"Removed scheduled email job: {job_id}")
            return True
        return False