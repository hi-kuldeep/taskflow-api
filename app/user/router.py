from app.user.dto.login_dto import LoginResponse, LoginSchema
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.constant.response_model import SuccessResponseDict, SuccessResponseSchema
from app.core import get_db
from app.user.controller import create_user, login_user
from app.user.dto.user_dto import UserResponseSchema, UserSchema
from app.core.auth_route import PublicRoute
from app.utils.security import protected, optional_auth
from app.constant.exception import CustomException

user_routes = APIRouter(prefix="/user", tags=["User"], route_class=PublicRoute)


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


@user_routes.get(
    "/me",
    response_model=SuccessResponseSchema[UserResponseSchema],
    status_code=status.HTTP_200_OK,
)
@protected
def get_me(request: Request) -> SuccessResponseDict[UserResponseSchema]:
    user = request.state.user
    return {
        "message": "User profile fetched successfully!",
        "status": status.HTTP_200_OK,
        "data": user,
    }


@user_routes.get(
    "/test-optional",
    status_code=status.HTTP_200_OK,
)
@optional_auth
def test_optional(request: Request):
    user = getattr(request.state, "user", None)
    if user:
        return {
            "message": "Authenticated user access",
            "user": user,
        }
    return {
        "message": "Anonymous user access",
        "user": None,
    }

