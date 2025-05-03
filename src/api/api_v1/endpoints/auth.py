from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.api.dependecies import get_db
from src.schemas.token import Token
from src.schemas.user import UserCreate, UserResponse
from src.core.auth.dependencies import get_current_user
from src.services.auth import login_access_token, register

router = APIRouter()


@router.post("/login", response_model=Token)
def login_user(db: Session = Depends(get_db),
               form_data: OAuth2PasswordRequestForm = Depends()):
    return login_access_token(db=db, form_data=form_data)


@router.post("/register", response_model=UserResponse)
def register_user(*, db: Session = Depends(get_db), user_in: UserCreate):
    return register(db=db, user_in=user_in)


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user
