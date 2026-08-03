from datetime import date

from fastapi import HTTPException, status

from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import SalesSummaryResponse


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

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both from_date and to_date must be provided."
            )


        # Invalid date range
        if from_date > to_date:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="from_date cannot be after to_date."
            )


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