from fastapi import APIRouter, Depends, status
from app.tasks import create_task, get_tasks , get_task_by_id, update_task, delete_task
from app.tasks.dtos import TaskSchema, TaskUpdateSchema
from app.core import get_db
task_routes = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_routes.post("/create", status_code=status.HTTP_201_CREATED)
def create_task_router(task_schema: TaskSchema , db = Depends(get_db)):
    return create_task(task_schema , db)

@task_routes.get("/", status_code=status.HTTP_200_OK)
def get_all_tasks(db = Depends(get_db)):
    return get_tasks(db)

@task_routes.get("/{task_id}" , status_code=status.HTTP_200_OK)
def get_task_by_id_router(task_id : str , db = Depends(get_db)):
    return get_task_by_id(task_id , db)

@task_routes.put("/{task_id}" , status_code=status.HTTP_200_OK)
def update_task_route( body : TaskUpdateSchema , task_id : str , db = Depends(get_db)):
    return update_task( body , task_id , db)

@task_routes.delete("/{task_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route( task_id : str , db = Depends(get_db)):
    return delete_task( task_id , db)