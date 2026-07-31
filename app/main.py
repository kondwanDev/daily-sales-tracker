from fastapi import FastAPI

from app.routers import auth , product, sale

app = FastAPI()

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(sale.router)