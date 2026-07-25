from typing import Any
from fastapi.responses import JSONResponse
from fastapi import Request

class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400, data: Any = None):
        self.message = message
        self.status_code = status_code
        self.data = data
        super().__init__(message)


async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, CustomException):
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal Server Error",
                "status": 500,
                "data": None
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "status": exc.status_code,
            "data": exc.data
        }
    )