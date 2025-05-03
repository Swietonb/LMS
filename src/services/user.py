from sqlalchemy.orm import Session
from src.crud.user import crud_user
from src.db.models.user import User, Role
from fastapi import HTTPException
from src.schemas.user import UserUpdate


def get_user_with_permission_check(db: Session, user_id: int, current_user: User) -> User:
    user = crud_user.get(db, obj_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found.')

    if user.id != current_user.id and not crud_user.is_admin(current_user):
        raise HTTPException(status_code=403, detail="You are not authorized to view this user's data.")

    return user


def update(*, db: Session, user_id: int, user_in: UserUpdate, current_user: User):
    user = crud_user.get(db, obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    if user.id != current_user.id and not crud_user.is_admin(current_user):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this user's data.",
        )
    if user_in.role is not None and user_in.role != user.role and not crud_user.is_admin(current_user):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this user's role.",
        )
    user = crud_user.update(db, user_id=user_id, user_request=user_in)
    return user


def delete(*, db: Session, user_id: int) -> None:

    user = crud_user.get(db, obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    crud_user.remove(db=db, obj_id=user_id)
    return None


def validate_user(user_id: int, db: Session, current_user: User):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f'User with id: {user_id} not found.')
    if user_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail='You can only access your own reservations')
