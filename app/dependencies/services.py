from app.repositories.user_repository import UserRepository
from app.dependencies.db import get_db
from fastapi import Depends
from app.services.auth_service import AuthService


def get_auth_service(conn = Depends(get_db)):

    repo = UserRepository(conn)
    
    return AuthService(repo)

