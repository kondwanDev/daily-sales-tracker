from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class SaleItemCreate(BaseModel):

    product_id: int

    quantity: int = Field(
        gt=0,
        description="Quantity sold must be greater than zero."
    )

    selling_price: Decimal = Field(
        gt=0,
        description="Selling price must be greater than zero."
    )


class SaleCreate(BaseModel):

    items: list[SaleItemCreate] = Field(
        min_length=1,
        description="A sale must contain at least one item."
    )

    @model_validator(mode="after")# This validator runs after the model is initialized, allowing us to access the items list and perform validation on it.
    def validate_unique_products(self):
        "Validate that each product in the sale is unique."

        product_ids = [item.product_id for item in self.items]

        if len(product_ids) != len(set(product_ids)):
            raise ValueError(
                "A product cannot appear more than once in a sale."
            )

        return self # return the model instance after validation