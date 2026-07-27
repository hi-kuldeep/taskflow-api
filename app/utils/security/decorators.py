from enum import Enum
from typing import Callable, TypeVar, Any

class AuthMode(str, Enum):
    PUBLIC = "public"
    PROTECTED = "protected"
    OPTIONAL = "optional"


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
