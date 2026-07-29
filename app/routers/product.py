from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_product_service
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    return service.create_product(product)

@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):
    return service.get_all_products()