# app/core/auth_route.py

from fastapi import Depends
from fastapi.routing import APIRoute

from app.utils.security import (
    AuthMode,
    verify_required_token,
    verify_optional_token,
)


class BaseAuthRoute(APIRoute):
    default_auth_mode = AuthMode.PUBLIC

    def __init__(self, path: str, endpoint, **kwargs):
        # Determine the auth mode for this endpoint, fallback to default
        auth_mode = getattr(endpoint, "__auth_mode__", self.default_auth_mode)

        dependencies = list(kwargs.get("dependencies") or [])

        if auth_mode == AuthMode.PROTECTED:
            dependencies.append(Depends(verify_required_token))
        elif auth_mode == AuthMode.OPTIONAL:
            dependencies.append(Depends(verify_optional_token))
        # For PUBLIC, we do not append any auth dependency

        kwargs["dependencies"] = dependencies

        super().__init__(
            path=path,
            endpoint=endpoint,
            **kwargs,
        )


class ProtectedRoute(BaseAuthRoute):
    default_auth_mode = AuthMode.PROTECTED


class PublicRoute(BaseAuthRoute):
    default_auth_mode = AuthMode.PUBLIC

