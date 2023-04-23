from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from app.crud import task as crud_task
from app.deps import get_current_user
from app.models import TaskStatus, User
from app.schemas import ErrorMessage, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    responses={404: {"model": ErrorMessage, "description": "The task was not found"}},
)


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate, current_user: User = Depends(get_current_user)
) -> TaskRead:
    new_task = await crud_task.create_task(payload, current_user)
    task = new_task.dict(exclude_none=True, exclude={"user"})
    user = new_task.user.email
    return TaskRead(user=user, **task)


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    completed: Optional[TaskStatus] = None,
    current_user: User = Depends(get_current_user),
) -> List[TaskRead]:
    tasks = await crud_task.retrieve_tasks(completed, current_user.id)
    return tasks


@router.get("/{id}", response_model=TaskRead)
async def get_task(
    id: PydanticObjectId, current_user: User = Depends(get_current_user)
) -> TaskRead:
    task = await crud_task.retrieve_task(id, current_user.id)
    return task


@router.patch("/{id}", response_model=TaskRead)
async def update_task(
    id: PydanticObjectId,
    payload: TaskUpdate,
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    payload_dict = payload.dict(exclude_none=True)
    updated_task = await crud_task.modify_task(id, payload_dict, current_user.id)
    return updated_task


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: PydanticObjectId, current_user: User = Depends(get_current_user)
):
    await crud_task.remove_task(id, current_user.id)
    return status.HTTP_204_NO_CONTENT
