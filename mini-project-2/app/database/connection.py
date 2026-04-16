from typing import Any, List, Optional
from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from models.users import User
from models.events import Event

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"

async def initialize_database():
    settings = Settings()
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Event, User]
    )

class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document: Document) -> None:
        await document.create()
        return

    async def get(self, id: Any) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()

    async def update(self, id: Any, body: Any) -> Any:
        doc_id = id
        des_body = body.dict(exclude_unset=True)
        
        update_query = {"$set": des_body}
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: Any) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True