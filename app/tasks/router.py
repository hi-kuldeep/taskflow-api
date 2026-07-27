from app.user.dto.user_dto import UserResponseSchema
from logging import log
from app.core.auth_route import ProtectedRoute
from app.utils.security import public, protected, optional_auth
from fastapi import APIRouter, Depends, status
from app.tasks import (
    create_task,
    get_task_by_user_id,
    get_task_by_id,
    update_task,
    delete_task,
)
from app.tasks.dtos import TaskSchema, TaskUpdateSchema, TaskResponseSchema
from app.core import get_db
from sqlalchemy.orm import Session
from app.constant.response_model import SuccessResponseSchema, SuccessResponseDict
from fastapi import Request
from app.constant.exception import CustomException
from app.user.models import UserModel

task_routes = APIRouter(prefix="/tasks", tags=["Tasks"], route_class=ProtectedRoute)


@task_routes.post(
    "/create",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
def create_task_router(
    task_schema: TaskSchema, request: Request, db: Session = Depends(get_db)
) -> SuccessResponseDict[TaskResponseSchema]:
    task = create_task(task_schema, db, request)
    return {
        "message": "Task created successfully!",
        "status": status.HTTP_201_CREATED,
        "data": task,
    }


@task_routes.get(
    "/",
    response_model=SuccessResponseSchema[list[TaskResponseSchema]],
    status_code=status.HTTP_200_OK,
)
def get_all_tasks(
    request: Request, db: Session = Depends(get_db)
) -> SuccessResponseDict:
    user: UserResponseSchema | None = getattr(request.state, "user", None)
    if not user:
        raise CustomException(
            "User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    tasks = get_task_by_user_id(db, user.id)
    return {
        "message": "Tasks fetched successfully!",
        "status": status.HTTP_200_OK,
        "data": tasks,
    }


@task_routes.get(
    "/{task_id}",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_task_by_id_router(task_id: str, db: Session = Depends(get_db)):
    task = get_task_by_id(task_id, db)
    return {
        "message": "Task fetched successfully!",
        "status": status.HTTP_200_OK,
        "data": task,
    }


@task_routes.put(
    "/{task_id}",
    response_model=SuccessResponseSchema[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def update_task_route(
    body: TaskUpdateSchema, task_id: str, db: Session = Depends(get_db)
):
    task = update_task(body, task_id, db)
    return {
        "message": "Task updated successfully!",
        "status": status.HTTP_200_OK,
        "data": task,
    }


@task_routes.delete(
    "/{task_id}",
    response_model=SuccessResponseSchema[None],
    status_code=status.HTTP_200_OK,
)
def delete_task_route(task_id: str, db: Session = Depends(get_db)):
    delete_task(task_id, db)
    return {
        "message": "Task deleted successfully!",
        "status": status.HTTP_200_OK,
        "data": None,
    }
