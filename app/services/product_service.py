from app.exceptions.product_exceptions import ProductNotFoundException, ProductAlreadyExistsException

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.unit_of_work.unit_of_work import UnitOfWork


class ProductService:

    def __init__(self, repo: ProductRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    def create_product(self, product: ProductCreate):

       product.name = product.name.strip()
       with self.uow:
        existing_product = self.repo.get_product_by_name(
            product.name
        )

        if existing_product:
            raise ProductAlreadyExistsException(product.name)
        
        product_data = product.model_dump()

        new_product = self.repo.create_product(product_data)

        self.uow.commit()

        return new_product
    

    def get_products(self, name: str | None = None, page: int = 1, per_page: int = 20):

      offset = (page - 1) * per_page

      products = self.repo.get_products(name, offset, per_page)

      return products

    def get_product_by_id(self, product_id: int):

      product = self.repo.get_product_by_id(product_id)

      if not product:
        raise ProductNotFoundException(product_id)

      return product

    def update_product(
    self,
    product_id: int,
    product: ProductUpdate
):

     with self.uow:

        existing_product = self.repo.get_product_by_id(product_id)

        if existing_product is None:
            raise ProductNotFoundException(product_id)

        # Only check duplicates if the client is changing the name.
        if product.name is not None:

            product.name = product.name.strip()

            duplicate = self.repo.get_other_product_by_name(
                product.name,
                product_id
            )

            if duplicate:
                raise ProductAlreadyExistsException(product.name)

        product_data = product.model_dump()

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
           raise ProductNotFoundException(product_id)
          
          self.uow.commit()