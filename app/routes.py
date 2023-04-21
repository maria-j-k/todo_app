from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, status

from app import crud
from app.models import Task, TaskStatus
from app.schemas import ErrorMessage, TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate) -> Task:
    new_task = await crud.create_task(payload)
    return new_task


@router.get(
    "/tasks",
    response_model=List[TaskRead],
    responses={
        404: {"model": ErrorMessage, "description": "The task was not found"}
    },
)
async def get_tasks(completed: Optional[TaskStatus] = None) -> List[Task]:
    tasks = await crud.retrieve_tasks(completed)
    return tasks


@router.get(
    "/{id}",
    response_model=Task,
    responses={
        404: {"model": ErrorMessage, "description": "The task was not found"}
    },
)
async def get_task(id: PydanticObjectId) -> Task:
    task = await crud.retrieve_task(id)
    return task


@router.patch(
    "/{id}",
    response_model=Task,
    responses={
        404: {"model": ErrorMessage, "description": "The task was not found"}
    },
)
async def update_task(id: PydanticObjectId, payload: TaskUpdate) -> Task:
    payload_dict = payload.dict(exclude_none=True)
    updated_task = await crud.modify_task(id, payload_dict)
    return updated_task


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorMessage, "description": "The task was not found"}
    },
)
async def delete_task(id: PydanticObjectId):
    await crud.remove_task(id)
    return status.HTTP_204_NO_CONTENT
