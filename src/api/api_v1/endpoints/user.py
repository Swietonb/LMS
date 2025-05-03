from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from src.api.dependecies import get_db
from src.core.auth.dependencies import get_current_admin_user, get_current_user
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.crud.user import crud_user
from src.services.auth import register
from src.services.user import get_user_with_permission_check, delete, update
from starlette import status

router = APIRouter()


@router.get("/multi", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100,
               current_user=Depends(get_current_admin_user)):
    return crud_user.get_multi(db, skip=skip, limit=limit)


@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate,
                current_user=Depends(get_current_admin_user)):
    return register(db=db, user_in=user_in)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(*, db: Session = Depends(get_db), user_id: int = Path(..., gt=0),
              current_user=Depends(get_current_user)):
    return get_user_with_permission_check(db=db, user_id=user_id, current_user=current_user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(*, db: Session = Depends(get_db), user_id: int = Path(..., gt=0),
                user_in: UserUpdate, current_user=Depends(get_current_user)):
    return update(db=db, user_id=user_id, user_in=user_in, current_user=current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, db: Session = Depends(get_db), user_id: int = Path(..., gt=0),
                current_user=Depends(get_current_admin_user)):

    delete(db=db, user_id=user_id)
