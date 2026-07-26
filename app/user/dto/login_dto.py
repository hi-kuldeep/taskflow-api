import uuid
from app.user.dto.user_dto import UserResponseSchema, UsernameField, PasswordField
from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: UsernameField
    password: PasswordField


class LoginResponse(BaseModel):
    user: UserResponseSchema
    token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
