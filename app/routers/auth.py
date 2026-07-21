from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.db import get_db
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn = Depends(get_db)
):

    repo = UserRepository(conn)

    service = AuthService(repo)

    return service.login(
        form_data.username,
        form_data.password
    )