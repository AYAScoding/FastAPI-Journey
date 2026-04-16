from typing import List, Optional
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from .events import Event

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]] = []

    class Settings:
        name = "users"

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@example.com",
                "password": "strongpassword123"
            }
        }