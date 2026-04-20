from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserPreferencesUpdate(BaseModel):
    dark_mode: bool = Field(default=False, description="user's dark mode preference")

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    dark_mode: bool
    created_at: datetime
