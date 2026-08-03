from fastapi import FastAPI

from app.routers import auth , product, sale, report

app = FastAPI()

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(sale.router)
app.include_router(report.router)