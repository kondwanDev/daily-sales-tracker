from fastapi import status

from app.exceptions.base import AppException


class ConflictException(AppException):
    """
    Base class for all resource conflict exceptions.
    """

    def __init__(
        self,
        message: str,
        error_code: str
    ):

        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code
        )