import motor.motor_asyncio
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.config import settings as test_settings
from app.deps import get_current_user
from app.main import app
from app.models import Task, User
from app.utils.auth_utils import get_hashed_password


@pytest_asyncio.fixture()
def cli(loop):
    client = motor.motor_asyncio.AsyncIOMotorClient(test_settings.mongo_url)
    return client


@pytest_asyncio.fixture()
def db(cli, loop):
    return cli["test_db"]


@pytest_asyncio.fixture(autouse=True)
async def api_client():
    """api client fixture."""
    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        server_name = test_settings.base_url
        async with AsyncClient(app=app, base_url=server_name) as ac:
            yield ac


@pytest_asyncio.fixture(autouse=True)
async def clean_db(loop, db):
    models = [User, Task]
    yield None

    for model in models:
        await model.get_motor_collection().drop()
        await model.get_motor_collection().drop_indexes()


def test_user():
    hashed_password = get_hashed_password("Pass4testUser&")
    user = User(
        id="6445864ee26a24f37c086ad0",
        email="test@test.pl",
        hashed_password=hashed_password,
    )
    return user


@pytest_asyncio.fixture(autouse=True)
async def test_current_user():
    app.dependency_overrides[get_current_user] = test_user
    return test_user()


@pytest_asyncio.fixture(autouse=True)
async def dummy_task():
    user = test_user()
    await user.insert()
    new_task = Task(title="dummy task", description="test task for test db", user=user)
    await new_task.insert()
    return new_task


@pytest_asyncio.fixture()
async def dummy_user():
    return test_user()


@pytest.fixture
def access_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDY4NjI5MDQsInN1YiI6IjY0NDNjZjc1YTE2MjE2ZGMxYzM4YmI4MyJ9.hHhRcqODQs8f6uhH22jZLxzD1rAC9uz8PsdRYSFfteY"  # noqa


@pytest.fixture
def auth_headers(access_token) -> dict:
    return {"Authorization": f"Bearer {access_token}"}
