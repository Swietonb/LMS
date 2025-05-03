from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description='Username')
    email: EmailStr = Field(..., description='User email')
    role: UserRole = Field(default=UserRole.USER, description='User role (user/admin)')


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description='Plain text password')


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50, description='Username')
    email: EmailStr | None = Field(None, description='User email')
    password: str | None = Field(None, min_length=8, description='Plain text password')
    role: UserRole | None = Field(None, description='User role (user/admin)')


class UserResponse(UserBase):
    id: int
    is_active: bool = True

    model_config = {'from_attributes': True}


class UserInDB(UserResponse):
    hashed_password: str
