from datetime import date

from fastapi import APIRouter, Depends

from app.schemas.report_schema import SalesSummaryResponse
from app.services.report_service import ReportService
from app.dependencies.services import get_report_service
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/sales-summary",
    response_model=SalesSummaryResponse
)
def get_sales_summary(
    from_date: date | None = None,
    to_date: date | None = None,
    current_user = Depends(get_current_user),
    service: ReportService = Depends(get_report_service)
):

    return service.get_sales_summary(
        user_id=current_user["id"],
        from_date=from_date,
        to_date=to_date
    )