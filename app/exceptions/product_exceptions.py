from app.exceptions.not_found import NotFoundException
from app.exceptions.conflict import ConflictException


class ProductNotFoundException(NotFoundException):
    """
    Raised when a requested product does not exist.
    """

    def __init__(self, product_id: int):

        self.product_id = product_id

        super().__init__(
            message=f"Product with ID {product_id} not found.",
            error_code="PRODUCT_NOT_FOUND"
        )


class ProductAlreadyExistsException(ConflictException):
    """
    Raised when trying to create a product that already exists.
    """

    def __init__(self, product_name: str):

        self.product_name = product_name

        super().__init__(
            message=f"Product with name '{product_name}' already exists.",
            error_code="PRODUCT_ALREADY_EXISTS"
        )