from src.crud.base import CRUDBase
from src.db.models import Review
from src.schemas.review import ReviewRequest
from sqlalchemy.orm import Session
from typing import Type, Any
from typing_extensions import override


class CRUDReview(CRUDBase[Review, ReviewRequest, ReviewRequest]):
    def get_by_book(self, db: Session, *, book_id: int) -> list[Type[Review]]:
        self.validate_book(book_id=book_id, db=db)
        return db.query(self.model).filter(self.model.book_id == book_id).all()

    def get_by_user(self, db: Session, *, user_id: int) -> list[Type[Review]]:
        self.validate_user(user_id=user_id, db=db)
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def get_by_rating(self, db: Session, *, rating: int) -> list[Type[Review]]:
        return db.query(self.model).filter(self.model.rating == rating).all()

    @override
    def create(self, db: Session, *, obj_request: ReviewRequest) -> Review:
        self.validate_user(user_id=obj_request.user_id, db=db)
        self.validate_book(book_id=obj_request.book_id, db=db)
        return super().create(db=db, obj_request=obj_request)

    @override
    def update(self, db: Session, *, obj_id: int,
               obj_request: ReviewRequest | dict[str, Any]) -> Review | None:
        self.validate_user(user_id=obj_request.user_id, db=db)
        self.validate_book(book_id=obj_request.book_id, db=db)
        return super().update(db=db, obj_id=obj_id, obj_request=obj_request)


crud_review = CRUDReview(Review)
