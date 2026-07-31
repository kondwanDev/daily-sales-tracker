from decimal import Decimal

from fastapi import HTTPException, status

from app.repositories.sale_repository import SaleRepository
from app.schemas.sale_schema import SaleCreate
from app.unit_of_work.unit_of_work import UnitOfWork


class SaleService:

    def __init__(
        self,
        repo: SaleRepository,
        uow: UnitOfWork
    ):
        self.repo = repo
        self.uow = uow

    def create_sale(
        self,
        sale: SaleCreate,
        user_id: int
    ):

        with self.uow:

            created_sale = self.repo.create_sale(user_id)

            total_amount = Decimal("0")

            for item in sale.items:

                if not self.repo.product_exists(item.product_id):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product with ID {item.product_id} not found."
                    )

                self.repo.add_sale_item(
                    sale_id=created_sale["id"],
                    product_id=item.product_id,
                    quantity=item.quantity,
                    selling_price=item.selling_price
                )

                total_amount += (
                    item.quantity * item.selling_price
                )

            updated_sale = self.repo.update_sale_total(
                sale_id=created_sale["id"],
                total_amount=total_amount
            )

            self.uow.commit()

            return updated_sale