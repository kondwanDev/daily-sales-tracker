from fastapi import status

from app.exceptions.base import AppException


class NotFoundException(AppException):
    """
    Base class for all 'resource not found' exceptions.
    """

    def __init__(
        self,
        message: str,
        error_code: str
    ):

        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code
        )