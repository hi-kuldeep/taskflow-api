from app.user.dto.login_dto import LoginResponse, LoginSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.constant.response_model import SuccessResponseDict, SuccessResponseSchema
from app.core import get_db
from app.user.controller import create_user, login_user
from app.user.dto.user_dto import UserResponseSchema, UserSchema

user_routes = APIRouter(prefix="/user", tags=["User"])


@user_routes.post(
    "/register",
    response_model=SuccessResponseSchema[UserResponseSchema],
    status_code=status.HTTP_201_CREATED,
)
def create_user_router(
    user_schema: UserSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict[UserResponseSchema]:
    user = create_user(user_schema, db)
    return {
        "message": "User created successfully!",
        "status": status.HTTP_201_CREATED,
        "data": user,
    }


@user_routes.post(
    "/login",
    response_model=SuccessResponseSchema[LoginResponse],
    status_code=status.HTTP_200_OK,
)
def login_user_router(
    body: LoginSchema, db: Session = Depends(get_db)
) -> SuccessResponseDict[LoginResponse]:
    data = login_user(body, db)

    return {
        "message": "User login successfully!",
        "status": status.HTTP_200_OK,
        "data": data,
    }
