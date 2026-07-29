from decimal import Decimal

from pydantic import BaseModel, Field

from datetime import datetime


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100) # ..., = required field
    category: str | None = Field(default=None, max_length=100)
    default_price: Decimal = Field(..., gt=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str | None
    default_price: Decimal
    created_at: datetime

class ProductUpdate(BaseModel):
    name: str
    category: str
    default_price: Decimal