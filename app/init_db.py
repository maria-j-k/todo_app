import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Task


async def init_db() -> None:
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(database=client.ToDo, document_models=[Task])
