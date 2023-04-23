from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models import Task, TaskStatus, User
from app.schemas import TaskCreate


async def create_task(payload: TaskCreate, user: User) -> Task:
    new_task = Task(user=user, **payload.dict())
    task = await new_task.insert()
    return task


async def retrieve_tasks(
    completed: Optional[TaskStatus], user_id: PydanticObjectId
) -> List[Task]:
    if completed:
        return await Task.find(
            Task.status == completed.value,
            Task.user.id == user_id,
            fetch_links=True,
        ).to_list()
    tasks = await Task.find(Task.user.id == user_id, fetch_links=True).to_list()
    return tasks


async def retrieve_task(id: PydanticObjectId, user_id: PydanticObjectId) -> Task:
    task = await Task.get(id, fetch_links=True)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if task.user.id != user_id:
        task = None
    return task


async def remove_task(id: PydanticObjectId, user_id: PydanticObjectId) -> None:
    task = await retrieve_task(id, user_id)
    await task.delete()


async def modify_task(
    id: PydanticObjectId, data: dict, user_id: PydanticObjectId
) -> Task:
    task = await retrieve_task(id, user_id)
    await task.update({"$set": data})
    return task
