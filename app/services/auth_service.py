from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.utils.security import verify_password, hash_password
from app.schemas.auth_schema import RegisterRequest, UserResponse
from app.utils.jwt import create_access_token
    


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo


    def login(self, username, password):

        user = self.repo.get_user_by_username(username) #self.repo because function get is in repo

        if not user:
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

        password_valid = verify_password(
        password,
        user["password_hash"]
    )

        if not password_valid:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

        token = create_access_token(
        {
            "sub": str(user["id"]),
            "role": user["role"]
        }
    )

        return {
        "access_token": token,
        "token_type": "bearer"

    }

        
    def register(self, data: RegisterRequest):

     existing_user = self.repo.get_user_by_username(data.username)

     if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )

     hashed_password = hash_password(data.password)

     user = self.repo.create_user(
        full_name=data.full_name,
        username=data.username,
        password_hash=hashed_password
    )

     return user

