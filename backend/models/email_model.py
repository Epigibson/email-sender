from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import random
import string
import email
from email.mime.text import MIMEText
import json

class EmailStatus(str, Enum):
    RECIEVED = "recieved"
    SENT = "sent"
    DRAFT = "draft"
    DELETED = "deleted"

class EmailMessage(Document):
    message_id: str
    from_email: EmailStr
    to_email: EmailStr
    subject: str
    body: str
    html: Optional[str] = None
    status: EmailStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False
    user_id: str  # ID del dueño del buzón
    raw_message: Optional[str] = None  # Mensaje en formato raw
    headers: Dict[str, Any] = Field(default_factory=dict)
    attachments: List[Dict[str, Any]] = Field(default_factory=list)

    class Settings:
        name = "email_messages"
        indexes = [
            "message_id",
            "to_email",
            "user_id",
            "status",
            "created_at"
        ]

    @classmethod
    def generate_message_id(cls, domain: str) -> str:
        """Genera un ID único para el mensaje"""
        rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        return f"<{int(datetime.utcnow().timestamp())}.{rand_str}@{domain}>"