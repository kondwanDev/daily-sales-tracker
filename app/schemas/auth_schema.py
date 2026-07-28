from pydantic import BaseModel, Field
from datetime import datetime


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    role: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str