from pydantic import ConfigDict
import uuid
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    username: str = Field(
        ...,
        description="User name",
        min_length=3,
        max_length=50,
    )
    email: EmailStr = Field(
        ...,
        description="User email",
    )
    password: str = Field(
        ...,
        description="User password",
        min_length=6,
        max_length=20,
    )


# class UserResponseSchema(UserSchema):
#     id: uuid.UUID
#     model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(BaseModel):
    id: uuid.UUID
    username: str = Field(..., description="User name")
    email: EmailStr = Field(..., description="User email")
    is_active: bool = Field(..., description="Is user active")
    is_email_verified: bool = Field(..., description="Is user email verified")
    created_at: datetime = Field(..., description="Created timestamp")
    updated_at: datetime = Field(..., description="Updated timestamp")
    model_config = ConfigDict(from_attributes=True)
