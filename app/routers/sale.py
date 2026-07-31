from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_sale_service
from app.schemas.sale_schema import SaleCreate
from app.dependencies.auth import get_current_user
from app.services.sale_service import SaleService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_sale(
    sale: SaleCreate,
    current_user=Depends(get_current_user),
    service: SaleService = Depends(get_sale_service)
):

    return service.create_sale(
        sale=sale,
        user_id=current_user["id"]
    )