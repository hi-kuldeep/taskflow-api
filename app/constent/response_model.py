from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
T = TypeVar('T')

class SuccessResponseSchema(BaseModel , Generic[T]):
    message : Optional[str] = ''
    status : int
    data : T | None = None
    

class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponseSchema(BaseModel):
    status : int
    error : str | None = None
    message : Optional[str] = ''
    details: Optional[list[ValidationErrorDetail]] = None
