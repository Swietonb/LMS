from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.crud.user import crud_user
from src.core.config import settings
from datetime import timedelta
from src.core.auth.jwt import create_access_token
from src.schemas.user import UserCreate


def login_access_token(
        db: Session, form_data: OAuth2PasswordRequestForm):
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account inactive.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


def register(*, db: Session, user_in: UserCreate):
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email address already exists."
        )

    username_exists = crud_user.get_by_username(db, username=user_in.username)
    if username_exists:
        raise HTTPException(
            status_code=400,
            detail="Username already exists."
        )

    user = crud_user.create(db, user_request=user_in)
    return user

