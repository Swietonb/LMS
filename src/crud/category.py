from src.crud.base import CRUDBase
from src.schemas.category import CategoryRequest
from src.db.models.category import Category
from sqlalchemy.orm import Session
from sqlalchemy import func


class CRUDCategory(CRUDBase[Category, CategoryRequest, CategoryRequest]):

    def get_by_name(self, db: Session, *, category_name: str) -> Category | None:
        return db.query(self.model).filter(func.lower(self.model.name) == category_name.lower()).first()


crud_category = CRUDCategory(Category)
