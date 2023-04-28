import pytest

from app.config import settings

URL = f"{settings.base_url}/auth/"


@pytest.mark.asyncio
async def test_signup(api_client) -> None:
    payload = {
        "email": "created@test.pl",
        "password": "Pass4testUser&",
    }
    url = f"{URL}signup"
    response = await api_client.post(url, json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]
    assert response.json()["external_identifier"] is None
    assert response.json()["hashed_password"]
    assert response.json()["hashed_password"] != payload["password"]


@pytest.mark.asyncio
async def test_login(api_client) -> None:
    payload = {
        "username": "test@test.pl",
        "password": "Pass4testUser&",
    }
    url = f"{URL}login"
    response = await api_client.post(url, data=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_request_password_reset(mocker, api_client, dummy_user) -> None:
    payload = {"email": dummy_user.email}
    mocked_email_service = mocker.patch(
        "app.routes.auth.send_message", return_value=None
    )
    response = await api_client.post(f"{URL}reset_request", json=payload)

    assert response.status_code == 204
    assert mocked_email_service.called
