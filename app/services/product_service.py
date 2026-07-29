from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate


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
    

    def get_all_products(self):

      products = self.repo.get_all_products()

      return products  