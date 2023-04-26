from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models import Task, User


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client.ToDo, document_models=[Task, User])
