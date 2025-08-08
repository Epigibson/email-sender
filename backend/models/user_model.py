# models/user.py
from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional

class User(Document):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    hashed_password: str
    disabled: bool = False

    class Settings:
        name = "users"