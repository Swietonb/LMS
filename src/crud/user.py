from src.core.auth.password import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.db.models import User
from src.db.models.user import Role
from src.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from typing import Any
from typing_extensions import override


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> User | None:
        return db.query(self.model).filter(self.model.username == username).first()

    @override
    def create(self, db: Session, *, user_request: UserCreate) -> User:
        obj_data = user_request.model_dump()

        password = obj_data.pop("password")
        obj_data["hashed_password"] = get_password_hash(password)

        db_obj = User(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, user_id: int, user_request: UserUpdate | dict[str, Any]) -> User:
        if isinstance(user_request, dict):
            update_data = user_request
        else:
            update_data = user_request.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, obj_id=user_id, obj_request=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_admin(user: User) -> bool:
        return user.role == Role.ADMIN


crud_user = CRUDUser(User)
