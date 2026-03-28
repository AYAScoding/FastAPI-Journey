from typing import List, Optional
from beanie import Document
from pydantic import BaseModel

class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Workshop",
                "image": "https://linktoimage.com/image.png",
                "description": "A hands-on session on Beanie and MongoDB.",
                "tags": ["python", "fastapi", "mongodb"],
                "location": "Virtual"
            }
        }

class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated FastAPI Workshop",
                "tags": ["python", "beanie"]
            }
        }