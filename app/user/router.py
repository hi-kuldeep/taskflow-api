from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.constant.response_model import SuccessResponseDict
from app.core import get_db
from app.user.controller import create_user
from app.user.dtos import UserResponseSchema, UserSchema

user_routes = APIRouter(prefix="/user", tags=["User"])


@user_routes.post("/register", status_code=status.HTTP_201_CREATED)
def create_user_router(
    user_schema: UserSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict[UserResponseSchema]:
    user = create_user(user_schema, db)
    return {
        "message": "User created successfully!",
        "status": status.HTTP_201_CREATED,
        "data": user,
    }
