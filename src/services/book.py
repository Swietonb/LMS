from sqlalchemy.orm import Session
from src.db.models.book import Book
from fastapi import HTTPException


def validate_book(book_id: int, db: Session):
    book_model = db.query(Book).filter(Book.id == book_id).first()
    if book_model is None:
        raise HTTPException(status_code=404, detail=f'Book with id: {book_id} not found.')
