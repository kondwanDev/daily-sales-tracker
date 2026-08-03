from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.unit_of_work.unit_of_work import UnitOfWork


class ProductService:

    def __init__(self, repo: ProductRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    def create_product(self, product: ProductCreate):
       
       with self.uow:
        existing_product = self.repo.get_product_by_name(
            product.name
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists"
            )

        new_product = self.repo.create_product(product)

        self.uow.commit()

        return new_product
    

    def get_products(self, name: str | None = None, page: int = 1, per_page: int = 20):

      offset = (page - 1) * per_page

      products = self.repo.get_products(name, offset, per_page)

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
     with self.uow:
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

      self.uow.commit()

      return updated_product

    def delete_product(self, product_id: int):

        with self.uow:

          deleted = self.repo.soft_delete_product(product_id)

          if not deleted:
           raise HTTPException(
            status_code=404,
            detail="Product not found."
        )
          self.uow.commit()