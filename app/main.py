from fastapi import FastAPI

from app.routers import auth , product

app = FastAPI()

app.include_router(auth.router)
app.include_router(product.router)