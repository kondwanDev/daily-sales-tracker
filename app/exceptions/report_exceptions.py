from app.exceptions.bad_request import BadRequestException


class InvalidDateRangeException(BadRequestException):
    """
    Raised when from_date is later than to_date.
    """

    def __init__(self):

        super().__init__(
            message="from_date cannot be after to_date.",
            error_code="INVALID_DATE_RANGE"
        )



class MissingDateRangeException(BadRequestException):
    """
    Raised when only one date is provided.
    """

    def __init__(self):

        super().__init__(
            message="Both from_date and to_date must be provided.",
            error_code="MISSING_DATE_RANGE"
        )