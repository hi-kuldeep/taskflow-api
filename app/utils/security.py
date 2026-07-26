from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Callable, TypeVar, Any
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash
from fastapi import Request, status

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


def verify_required_token(request: Request) -> dict:
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
    request.state.user = payload
    return payload


def verify_optional_token(request: Request) -> dict | None:
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
    request.state.user = payload
    return payload


def get_current_user(request: Request) -> dict:
    if not hasattr(request.state, "user") or request.state.user is None:
        return verify_required_token(request)
    return request.state.user


def get_optional_user(request: Request) -> dict | None:
    if not hasattr(request.state, "user"):
        return verify_optional_token(request)
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

