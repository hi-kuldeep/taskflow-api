from app.constant.exception import CustomException
from app.tasks.dtos import TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session
from app.tasks.models import TaskModel
from fastapi import  HTTPException, status
def create_task(body: TaskSchema , db:Session):
    data = body.model_dump()
    new_task = TaskModel(
        **data
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return tasks

    
def get_task_by_id(task_id : str , db:Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise CustomException(
            "Task not found." ,
             status_code=status.HTTP_404_NOT_FOUND
             )
    return task

def update_task(  body : TaskUpdateSchema, task_id : str, db : Session):
    task = db.query(TaskModel).get(task_id)
    if not task:
        raise CustomException(
            "Task not found.",
             status_code=status.HTTP_404_NOT_FOUND
             )
    
    task_dict = body.model_dump(exclude_unset=True)
    
    for field , value in task_dict.items():
        setattr(task, field, value)
        
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(task_id: str , db : Session):
    print("task_id -> " , task_id )
    task = db.query(TaskModel).get(task_id)
    print("task -> " , task)
    if not task:
        raise CustomException(
            "Task not found.",
             status_code=status.HTTP_404_NOT_FOUND
             )
    db.delete(task)
    db.commit()
    return None