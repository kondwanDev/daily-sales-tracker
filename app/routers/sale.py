from fastapi import APIRouter, Depends, Query, status

from app.dependencies.services import get_sale_service
from app.schemas.sale_schema import SaleCreate, SaleListResponse, SaleDetailResponse
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

@router.get(
    "",
    response_model=list[SaleListResponse]
)
def get_sales(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    service: SaleService = Depends(get_sale_service)
):

    return service.get_sales(
        user_id=current_user["id"],
        page=page,
        per_page=per_page
    )


@router.get(
    "/{sale_id}",
    response_model=SaleDetailResponse
)
def get_sale(
    sale_id: int,
    current_user = Depends(get_current_user),
    service: SaleService = Depends(get_sale_service)
):

    return service.get_sale_by_id(
        sale_id=sale_id,
        user_id=current_user["id"]
    )