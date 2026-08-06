from fastapi import FastAPI

from app.exceptions.base import AppException
from app.exceptions.handlers import app_exception_handler
from app.routers import auth , product, sale, report

app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(sale.router)
app.include_router(report.router)