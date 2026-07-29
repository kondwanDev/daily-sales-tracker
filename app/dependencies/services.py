from fastapi import Depends

from app.dependencies.db import get_db

from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository

from app.services.auth_service import AuthService
from app.services.product_service import ProductService 


def get_auth_service(conn = Depends(get_db)):

    repo = UserRepository(conn)
    
    return AuthService(repo)


def get_product_service(conn=Depends(get_db)):

    repo = ProductRepository(conn)

    return ProductService(repo)

