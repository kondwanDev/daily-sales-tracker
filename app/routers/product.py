from fastapi import APIRouter, Depends, status
from fastapi import Query

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_product_service
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
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
@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    name: str | None = Query(default=None),
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):

    return service.get_products(name)

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):

    return service.get_product_by_id(product_id)

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):

    return service.update_product(product_id, product)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_user)
):

    service.delete_product(product_id) # no return statement needed for 204 No Content response