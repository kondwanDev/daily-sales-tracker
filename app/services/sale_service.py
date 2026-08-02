from decimal import Decimal

from fastapi import HTTPException, status

from app.repositories.sale_repository import SaleRepository
from app.schemas.sale_schema import SaleCreate, SaleItemResponse, SaleDetailResponse
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

    def get_sales(
    self,
    user_id: int,
    page: int,
    per_page: int
): 
            offset = (page - 1) * per_page

            return self.repo.get_sales(user_id,
                                       limit=per_page,
                                       offset=offset)


    def get_sale_by_id(
    self,
    sale_id: int,
    user_id: int
):

        rows = self.repo.get_sale_by_id(
        sale_id,
        user_id
    )
        
        if not rows:
         raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    # Construct the SaleDetailResponse object from the rows returned by the repository
    # rows[0] contains the sale details, and the rest of the rows contain the sale items
        sale = {
        "id": rows[0]["id"],
        "total_amount": rows[0]["total_amount"],
        "sale_date": rows[0]["sale_date"],
        "items": []
    }


        for row in rows:

         item = SaleItemResponse(
            product_id=row["product_id"],
            product_name=row["product_name"],
            default_price=row["default_price"],
            quantity=row["quantity"],
            selling_price=row["selling_price"]
        ) 
         

         sale["items"].append(item)

        return SaleDetailResponse(**sale) # using **sale to unpack the dictionary into keyword arguments for the SaleDetailResponse model