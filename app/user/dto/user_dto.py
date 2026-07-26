import uuid
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime


UsernameField = Annotated[
    str,
    Field(
        ...,
        description="User name",
        min_length=3,
        max_length=50,
    ),
]

PasswordField = Annotated[
    str,
    Field(
        ...,
        description="User password",
        min_length=6,
        max_length=20,
    ),
]


class UserSchema(BaseModel):
    username: UsernameField
    email: EmailStr = Field(
        ...,
        description="User email",
    )
    password: PasswordField


class UserResponseSchema(BaseModel):
    id: uuid.UUID
    username: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email")
    is_active: bool = Field(..., description="Is user active")
    is_email_verified: bool = Field(..., description="Is user email verified")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    model_config = ConfigDict(from_attributes=True)
