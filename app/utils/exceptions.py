import http
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.constant.response_model import ErrorResponseSchema
from app.constant.exception import CustomException, custom_exception_handler


def register_error_handlers(app: FastAPI) -> None:
    """Registers global exception handlers for the FastAPI application."""

    # Register custom exception handler
    app.add_exception_handler(CustomException, custom_exception_handler)

    # Global exception handler to intercept standard HTTP exceptions (e.g., 404, 403, 401).
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        try:
            error_phrase = http.HTTPStatus(exc.status_code).phrase
        except ValueError:
            error_phrase = "Error"

        error_response = ErrorResponseSchema(
            status=exc.status_code,
            error=error_phrase,
            message=exc.detail if isinstance(exc.detail, str) else "An HTTP exception occurred."
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )

    # Global exception handler to catch request validation errors thrown by FastAPI / Pydantic
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        error_details = exc.errors()
        
        formatted_errors = []
        details = []
        for err in error_details:
            loc = err.get("loc", [])
            # Remove request source keywords like "body", "query", etc.
            field_path = [str(item) for item in loc if item not in ("body", "query", "path", "header", "cookie")]
            field_name = ".".join(field_path) if field_path else "Field"
            
            msg = err.get("msg", "")
            # Format typical Pydantic messages to be user-friendly
            if msg == "Field required":
                clean_msg = f"{field_name} is required"
            elif msg.startswith("String "):
                clean_msg = msg.replace("String", field_name, 1)
            elif msg.startswith("Input should be "):
                clean_msg = msg.replace("Input should be", f"{field_name} should be", 1)
            else:
                clean_msg = f"{field_name}: {msg}"
                
            formatted_errors.append(clean_msg)
            details.append({
                "field": field_name,
                "message": clean_msg
            })
                
        # If there is only one validation error, display it directly in the message.
        # Otherwise, set a general "Validation failed." message.
        error_message = "Validation failed." if len(formatted_errors) > 1 else formatted_errors[0]
        
        error_response = ErrorResponseSchema(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error="Validation Error",
            message=error_message,
            details=details
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump()
        )
