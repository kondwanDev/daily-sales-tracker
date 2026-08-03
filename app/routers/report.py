from datetime import date

from fastapi import APIRouter, Depends, Query

from app.schemas.report_schema import SalesSummaryResponse, SalesHistoryItemResponse
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
    from_date: date | None =Query(None,
                                  description= "Start date (YYYY-MM-DD)"
                                  ),
    to_date: date | None =Query(None,
                                 description="End date (YYYY-MM-DD)"),
    current_user = Depends(get_current_user),
    service: ReportService = Depends(get_report_service)
):

    return service.get_sales_summary(
        user_id=current_user["id"],
        from_date=from_date,
        to_date=to_date
    )


@router.get(
    "/sales-history",
    response_model=list[SalesHistoryItemResponse]
)
def get_sales_history(
    from_date: date | None = Query(
        None,
        description="Start date (YYYY-MM-DD)"
    ),

    to_date: date | None = Query(
        None,
        description="End date (YYYY-MM-DD)"
    ),

    current_user = Depends(get_current_user),

    service: ReportService = Depends(get_report_service)
):

    return service.get_sales_history(
        user_id=current_user["id"],
        from_date=from_date,
        to_date=to_date
    )