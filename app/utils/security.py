from typing import Annotated
from app.user.models import UserModel
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Callable, TypeVar, Any
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash
from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from app.core import get_db
from app.core.config import settings
from app.constant.exception import CustomException

password_hash = PasswordHash.recommended()


class AuthMode(str, Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    OPTIONAL = "optional"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        raise CustomException(
            "Token expired",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except InvalidTokenError:
        raise CustomException(
            "Invalid token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


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


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Any:
    if not hasattr(request.state, "user") or request.state.user is None:
        return verify_required_token(request, db)
    return request.state.user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Any:
    if not hasattr(request.state, "user"):
        return verify_optional_token(request, db)
    return request.state.user


F = TypeVar("F", bound=Callable[..., Any])


def public(func: F) -> F:
    setattr(func, "__auth_mode__", AuthMode.PUBLIC)
    return func


def protected(func: F) -> F:
    setattr(func, "__auth_mode__", AuthMode.PROTECTED)
    return func


def optional_auth(func: F) -> F:
    setattr(func, "__auth_mode__", AuthMode.OPTIONAL)
    return func


def get_current_user(request: Request) -> UserModel:
    user = getattr(request.state, "user", None)
    if not user:
        raise CustomException(
            "User not authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return user


DB_Session = Annotated[
    Session,
    Depends(get_db),
]


CurrentUser = Annotated[
    UserModel,
    Depends(get_current_user),
]
