from pydantic import BaseModel, Field
from pydantic_partial import PartialModelMixin

class TaskSchema(PartialModelMixin, BaseModel):
    title: str = Field(
        ...,
        description="Title of the task",
        min_length=3,
        max_length=100,
    )
    description: str = Field(
        description="Description of the task",
        min_length=3,
        max_length=255,
    )
    is_completed: bool = Field(
        False,
        description="Is the task completed?",
    )



TaskUpdateSchema = TaskSchema.model_as_partial() 
