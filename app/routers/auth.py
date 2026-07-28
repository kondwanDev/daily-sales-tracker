from fastapi import APIRouter, Depends,status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_auth_service
from app.schemas.auth_schema import RegisterRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):

    return service.register(data)

@router.post("/login", response_model=TokenResponse)

def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):

        return service.login(
        form_data.username,
        form_data.password
    ) 

