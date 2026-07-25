from typing import Any, Generic, Optional, TypeVar, TypedDict
from pydantic import BaseModel
T = TypeVar('T')

class SuccessResponseDict(TypedDict , Generic[T]):
    message: str
    status: int
    data: T | None

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
