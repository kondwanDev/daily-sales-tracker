from app.exceptions.not_found import NotFoundException


class SaleNotFoundException(NotFoundException):
    """
    Raised when a requested sale does not exist.
    """

    def __init__(self, sale_id: int):

        self.sale_id = sale_id

        super().__init__(
            message=f"Sale with ID {sale_id} not found.",
            error_code="SALE_NOT_FOUND"
        )