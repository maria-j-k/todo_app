import motor.motor_asyncio
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import BaseSettings

from app.config import settings as main_settings
from app.main import app
from app.models import Task, User


class Settings(BaseSettings):
    mongodb_dsn: str = main_settings.mongo_test_db_url
    mongodb_db_name: str = "test_db"


@pytest.fixture
def test_settings():
    return Settings()


@pytest.fixture()
def cli(test_settings, loop):
    client = motor.motor_asyncio.AsyncIOMotorClient(test_settings.mongodb_dsn)
    return client


@pytest.fixture()
def db(cli, test_settings, loop):
    return cli[test_settings.mongodb_db_name]


@pytest_asyncio.fixture(autouse=True)
async def api_client(clean_db):
    """api client fixture."""
    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        server_name = "https://localhost"
        async with AsyncClient(app=app, base_url=server_name) as ac:
            yield ac


@pytest.fixture(autouse=True)
async def clean_db(loop, db):
    models = [User, Task]
    yield None

    for model in models:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()


# from fastapi.testclient import TestClient
#
# import pytest
# import mongomock
# from beanie import init_beanie
#
# from app.main import app
# from app.models import Task, User
# from app.config import settings
# from typing import Dict
#
#
# async def init_test_db():
#     client = AsyncClient(app=app, base_url=settings.mongodb_url)
#
#     await init_beanie(database=client.to_do, document_models=[Task, User])
#


@pytest.fixture
def access_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDY4NjI5MDQsInN1YiI6IjY0NDNjZjc1YTE2MjE2ZGMxYzM4YmI4MyJ9.hHhRcqODQs8f6uhH22jZLxzD1rAC9uz8PsdRYSFfteY"  # noqa


#
# @pytest.fixture
# def async_client():
#     return AsyncClient(app=app, base_url="http://test")
#
#
@pytest.fixture
def auth_headers(access_token) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


#
#
# @pytest.fixture
# async def mongo_mock(monkeypatch, async_client):
#     await init_test_db()
#     #
#     # client = mongomock.MongoClient()
#     # db = async_client.get_database("to_do")
#     new_user = User(email="test@test.pl", hashed_password="$2b$12$nDyY5HeoUv..zNNRdHgIEuVe4tFrX7LMUL8apkjGylIHtFM9S43RW")
#     user = await new_user.insert()
#     # new_task = Task(title="dummy task", description="test task for test db")
#     # await new_task.insert()
#
#     def fake_db():
#         return db
#
#     monkeypatch.setattr("app.init_db", fake_db)
#
#
# @pytest.fixture
# def new_task():
#     return Task(title="newly created", description="whatever")
