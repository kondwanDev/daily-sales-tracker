from fastapi import Depends

from app.dependencies.db import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.sale_repository import SaleRepository
from app.repositories.report_repository import ReportRepository

from app.services.report_service import ReportService
from app.services.auth_service import AuthService
from app.services.product_service import ProductService 
from app.services.sale_service import SaleService
from app.unit_of_work.unit_of_work import UnitOfWork



def get_auth_service(conn = Depends(get_db)):

    repo = UserRepository(conn)
    
    return AuthService(repo)


def get_product_service(conn=Depends(get_db)):

    repo = ProductRepository(conn)

    uow = UnitOfWork(conn)

    return ProductService(repo, uow)


def get_sale_service(conn=Depends(get_db)):

    repo = SaleRepository(conn)

    uow = UnitOfWork(conn)

    return SaleService(repo, uow)


def get_report_service(conn=Depends(get_db)):

    repo = ReportRepository(conn)

    return ReportService(repo)
