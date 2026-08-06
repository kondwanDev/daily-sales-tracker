from fastapi import status

from app.exceptions.base import AppException


class BadRequestException(AppException):
    """
    Base class for all invalid client requests.
    """

    def __init__(
        self,
        message: str,
        error_code: str
    ):

        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code
        )