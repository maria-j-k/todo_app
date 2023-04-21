from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models import Task, TaskStatus


async def create_task(payload):
    new_task = Task(**payload.dict())
    task = await new_task.insert()
    return task


async def retrieve_tasks(completed: Optional[TaskStatus]) -> List[Task]:
    if completed:
        return await Task.find(Task.status == completed.value).to_list()
    tasks = await Task.all().to_list()
    return tasks


async def retrieve_task(id: PydanticObjectId) -> Task:
    task = await Task.get(id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


async def remove_task(id: PydanticObjectId) -> None:
    task = await retrieve_task(id)
    await task.delete()


async def modify_task(id: PydanticObjectId, data: dict) -> Task:
    task = await retrieve_task(id)
    await task.update({"$set": data})
    return task
