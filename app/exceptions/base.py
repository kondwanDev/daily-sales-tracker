from fastapi import status


class AppException(Exception):
    """
    Base class for all custom application exceptions.

    Every business exception in the project should inherit from this class.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str
    ):
        # Human-readable message returned to the client.
        self.message = message

        # HTTP status code that FastAPI should return.
        self.status_code = status_code

        # Machine-readable identifier for this error.
        self.error_code = error_code

        # Pass the message to Python's built-in Exception class.
        super().__init__(message)