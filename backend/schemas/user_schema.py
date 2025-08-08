# schemas/user_schema.py
from pydantic import EmailStr
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    hashed_password: str