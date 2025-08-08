from fastapi import APIRouter, HTTPException, status
from services.email_services import EmailService
from typing import List

router = APIRouter()


@router.post("/send-email")
async def send_email(to_emails: List[str], subject: str):
    try:
        return await EmailService.send_simple_message(to_emails, subject)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
