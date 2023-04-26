import pytest

from app.config import settings
from app.routes import task
from app.schemas import TaskCreate


@pytest.mark.asyncio
async def test_read_task(api_client, auth_headers: dict) -> None:
    payload = TaskCreate(title="created by test", description="test").dict()

    response = await api_client.post(
        f"{settings.base_url}/tasks/", headers=auth_headers, json=payload
    )
    assert response.status_code == 201


# @pytest.mark.asyncio
# async def test_get_access_token(api_client) -> None:
#     login_data = {
#         "username": "test@test.pl",
#         "password": "Qwe32ks!12345",
#     }
#     r = await api_client.post(f"{settings.base_url}/auth/login", data=login_data)
#     breakpoint()
#     tokens = r.json()
#     assert r.status_code == 200
#     assert "access_token" in tokens
#     assert tokens["access_token"]
