from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, repo: ProductRepository):
        self.repo = repo


    def create_product(self, product: ProductCreate):

        existing_product = self.repo.get_product_by_name(
            product.name
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists"
            )

        return self.repo.create_product(product)
    

    def get_products(self, name: str | None = None):

      products = self.repo.get_products(name)

      return products

    def get_product_by_id(self, product_id: int):

      product = self.repo.get_product_by_id(product_id)

      if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

      return product

    def update_product(
    self,
    product_id: int,
    product: ProductUpdate
):

     existing_product = self.repo.get_product_by_id(product_id)

     if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

     product_data = product.model_dump() #convert the ProductUpdate object to a dictionary for repo....

     updated_product = self.repo.update_product(
        product_id,
        product_data
    )

     return updated_product