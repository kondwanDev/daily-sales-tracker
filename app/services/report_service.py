from datetime import date

from app.exceptions.report_exceptions import InvalidDateRangeException, MissingDateRangeException
from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import ProductSalesResponse, SalesHistoryItemResponse, SalesSummaryResponse


class ReportService:

    def __init__(
        self,
        repo: ReportRepository
    ):
        self.repo = repo


    def get_sales_summary(
        self,
        user_id: int,
        from_date: date | None = None,
        to_date: date | None = None
    ) -> SalesSummaryResponse:

        # No dates provided → use today
        if from_date is None and to_date is None:

            from_date = date.today()
            to_date = date.today()


        # Only one date provided → invalid
        elif from_date is None or to_date is None:

            raise MissingDateRangeException()


        # Invalid date range
        if from_date > to_date:

            raise InvalidDateRangeException()


        result = self.repo.get_sales_summary(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date
        )


        return SalesSummaryResponse(
            from_date=from_date,
            to_date=to_date,
            total_sales=result["total_sales"],
            total_revenue=result["total_revenue"]
        )


    def get_sales_history(
    self,
    user_id: int,
    from_date: date | None = None,
    to_date: date | None = None
):

     if from_date is None and to_date is None:

        from_date = date.today()
        to_date = date.today()


     elif from_date is None or to_date is None:

        raise MissingDateRangeException()



     if from_date > to_date:

        raise InvalidDateRangeException()


     rows = self.repo.get_sales_history(
        user_id=user_id,
        from_date=from_date,
        to_date=to_date
    )


     return [
        SalesHistoryItemResponse(
            id=row["id"],
            total_amount=row["total_amount"],
            sale_date=row["sale_date"]
        )
        for row in rows
    ]

    def get_product_sales(
    self,
    user_id: int,
    from_date: date | None = None,
    to_date: date | None = None
):

     if from_date is None and to_date is None:

        from_date = date.today()
        to_date = date.today()


     elif from_date is None or to_date is None:

        raise MissingDateRangeException()
        


     if from_date > to_date:

        raise InvalidDateRangeException()


     rows = self.repo.get_product_sales(
        user_id=user_id,
        from_date=from_date,
        to_date=to_date
    )


     return [
        ProductSalesResponse(
            product_id=row["product_id"],
            product_name=row["product_name"],
            default_price=row["default_price"],
            quantity_sold=row["quantity_sold"],
            revenue=row["revenue"]
        )
        for row in rows
    ]
    