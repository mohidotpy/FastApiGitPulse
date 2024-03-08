from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.entities.exceptions import InvalidDataException
from app.repository.exceptions import ExternalAPIError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

async def invalid_data_exception_handler(request: Request, exc: InvalidDataException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
    )


async def external_api_error_handler(request: Request, exc: ExternalAPIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "external_api_detail_error": exc.external_api_detail_error},
    )
