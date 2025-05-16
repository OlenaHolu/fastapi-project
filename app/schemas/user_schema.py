from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional

class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    photo: Optional[HttpUrl] = None
    password: Optional[str] = Field(None, min_length=6, max_length=50)