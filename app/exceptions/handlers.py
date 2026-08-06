from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import AppException


async def app_exception_handler(
    request: Request, # the incoming HTTP request that caused the exception
    exc: AppException # the custom application exception object that was raised
):
    """
    Handles all custom application exceptions.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.message
        }
    )