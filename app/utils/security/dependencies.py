from typing import Annotated, Any
from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from app.core import get_db
from app.user.models import UserModel
from app.constant.exception import CustomException
from app.utils.security.token import verify_token


def verify_required_token(request: Request, db: Session = Depends(get_db)) -> Any:
    if hasattr(request.state, "user") and request.state.user is not None:
        return request.state.user

    authorization: str | None = request.headers.get("Authorization")

    if not authorization:
        raise CustomException(
            "Authorization token is missing",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise CustomException(
            "Invalid authorization header format",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    payload = verify_token(token)

    username = payload.get("sub")
    if not username:
        raise CustomException(
            "Invalid token payload",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    from app.user.models import UserModel

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise CustomException(
            "User not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.state.user = user
    return user


def verify_optional_token(request: Request, db: Session = Depends(get_db)) -> Any:
    if hasattr(request.state, "user"):
        return request.state.user

    authorization: str | None = request.headers.get("Authorization")

    if not authorization:
        request.state.user = None
        return None

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise CustomException(
            "Invalid authorization header format",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    payload = verify_token(token)

    username = payload.get("sub")
    if not username:
        raise CustomException(
            "Invalid token payload",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    from app.user.models import UserModel

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise CustomException(
            "User not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.state.user = user
    return user


def get_current_user(request: Request) -> UserModel:
    user = getattr(request.state, "user", None)
    if not user:
        raise CustomException(
            "User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return user


CurrentUser = Annotated[
    UserModel,
    Depends(get_current_user),
]
