from src.crud.base import CRUDBase
from src.db.models.book import Book
from src.db.models.category import Category
from src.schemas.book import BookRequest
from sqlalchemy.orm import Session
from src.db.models.association import book_category
from fastapi import HTTPException
from typing import Type
from typing_extensions import override
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


class CRUDBook(CRUDBase[Book, BookRequest, BookRequest]):

    def get_by_category(self, db: Session, *, category_id: int) -> list[Book]:
        return (db.query(self.model).join(book_category)  # type: ignore
                .filter(book_category.c.category_id == category_id).all())

    def get_by_author(self, db: Session, *, book_author: str) -> list[Type[Book]]:
        return db.query(self.model).filter(func.lower(self.model.author) == book_author.lower()).all()

    def get_by_title(self, db: Session, *, book_title: str) -> list[Book]:
        return db.query(self.model).filter(func.lower(self.model.title) == book_title.lower()).all()  # type: ignore

    def get_by_year(self, db: Session, *, book_year: int) -> list[Book]:
        return db.query(self.model).filter(self.model.year == book_year).all()  # type: ignore

    def get_by_availability(self, db: Session, *, book_availability: bool) -> list[Book]:
        return db.query(self.model).filter(self.model.availability == book_availability).all()  # type: ignore

    @override
    def create(self, db: Session, *, obj_request: BookRequest):
        category_ids = obj_request.category_ids
        book_data = obj_request.model_dump(exclude={'category_ids'})
        categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

        book_model = Book(**book_data, categories=categories)

        if len(categories) != len(category_ids):
            found_ids = [cat.id for cat in categories]
            missing_ids = [cat_id for cat_id in category_ids if cat_id not in found_ids]
            raise HTTPException(status_code=404, detail=f"Categories not found: {missing_ids}")

        db.add(book_model)
        try:
            db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail='Book with given ISBN already exists.')
        db.refresh(book_model)
        return book_model

    def add_category_to_book(self, db: Session, *, book_id: int, category_name: str) -> Book:
        book_model = self.get(db, obj_id=book_id)
        if book_model is None:
            raise HTTPException(status_code=404, detail='Book Not Found!')
        category = db.query(Category).filter(Category.name == category_name).first()
        if category is None:
            raise HTTPException(status_code=404, detail='Category Not Found!')
        if category not in book_model.categories:
            book_model.categories.append(category)
            db.commit()
        return book_model  # type: ignore

    @override
    def update(self, db: Session, *, obj_id: int, obj_request: BookRequest) -> Book | None:

        if obj_request.category_ids is not None:
            categories = db.query(Category).filter(Category.id.in_(obj_request.category_ids)).all()
            self.model.categories = categories

        return super().update(db, obj_id=obj_id, obj_request=obj_request)

    def delete_category_from_book(self, db: Session, *, obj_id: int, category_name: str) -> Book:
        book_model = self.get(db, obj_id=obj_id)
        if book_model is None:
            raise HTTPException(status_code=404, detail='Book Not Found!')
        category = db.query(Category).filter(Category.name == category_name).first()
        if category is None:
            raise HTTPException(status_code=404, detail='Category Not Found!')
        if category in book_model.categories:
            book_model.categories.remove(category)
            db.commit()
        return book_model  # type: ignore

    def search_books(self, db: Session, *, search_text: str) -> list[Book]:
        return db.query(self.model).filter(or_(  # type: ignore
            Book.title.ilike(f'%{search_text}%'),
            Book.author.ilike(f'%{search_text}%')
        )
        ).all()


crud_book = CRUDBook(Book)
