import pytest

from app.config import settings
from app.models import Task
from app.schemas import TaskCreate

URL = f"{settings.base_url}/tasks/"


@pytest.mark.asyncio
async def test_create_task(api_client, auth_headers: dict) -> None:
    payload = TaskCreate(title="created by test", description="test").dict()
    tasks = await Task.find_all().to_list()
    response = await api_client.post(URL, headers=auth_headers, json=payload)
    new_tasks = await Task.find_all().to_list()

    assert response.status_code == 201
    assert len(new_tasks) == len(tasks) + 1


@pytest.mark.asyncio
async def test_read_tasks(api_client, auth_headers: dict, dummy_task) -> None:
    response = await api_client.get(URL, headers=auth_headers)
    task_from_db = response.json()[0]
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert task_from_db["_id"] == str(dummy_task.id)
    assert task_from_db["title"] == dummy_task.title
    assert task_from_db["description"] == dummy_task.description


@pytest.mark.asyncio
async def test_read_single_task(api_client, auth_headers: dict, dummy_task) -> None:
    response = await api_client.get(url=f"{URL}{dummy_task.id}", headers=auth_headers)
    task_from_db = response.json()
    assert response.status_code == 200
    assert task_from_db["_id"] == str(dummy_task.id)
    assert task_from_db["title"] == dummy_task.title
    assert task_from_db["description"] == dummy_task.description


@pytest.mark.asyncio
async def test_update_single_task(api_client, auth_headers: dict, dummy_task):
    payload = {"status": "done"}
    response = await api_client.patch(
        url=f"{URL}{dummy_task.id}", headers=auth_headers, json=payload
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"


@pytest.mark.asyncio
async def test_delete_task(api_client, auth_headers: dict, dummy_task):
    response = await api_client.delete(
        url=f"{URL}{dummy_task.id}", headers=auth_headers
    )
    tasks = await Task.find_all().to_list()
    assert response.status_code == 204
    assert len(tasks) == 0
