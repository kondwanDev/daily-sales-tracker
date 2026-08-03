from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class SalesSummaryResponse(BaseModel):

    from_date: date
    to_date: date
    total_sales: int
    total_revenue: Decimal


class SalesHistoryItemResponse(BaseModel):

    id: int
    total_amount: Decimal
    sale_date: datetime

class ProductSalesResponse(BaseModel):

    product_id: int
    product_name: str
    quantity_sold: int
    revenue: Decimal
    default_price: Decimal

"""
   # Instead of repeating from and to everywhere later, we create one reusable schema
# we will add it later, if reporting grows more complex (many filters), introduce
class ReportFilter(BaseModel):

    from_date: date
    to_date: date 
"""
