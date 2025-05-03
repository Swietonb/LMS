from fastapi import APIRouter, Depends, Path

from src.core.auth.dependencies import get_current_admin_user
from src.schemas.book import BookResponse, BookRequest
from starlette import status
from sqlalchemy.orm import Session
from src.api.dependecies import get_db
from src.crud.book import crud_book
from src.db.models.book import Book


router = APIRouter()


@router.get('/multi', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_multi(skip: int = 0, limit: int = 5000, db: Session = Depends(get_db)):
    return crud_book.get_multi(db, skip=skip, limit=limit)


@router.get('/category/{category_id}', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_by_category(category_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return crud_book.get_by_category(db, category_id=category_id)


@router.get('/author/{author_name}', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_by_author(author_name: str = Path(min_length=3), db: Session = Depends(get_db)):
    return crud_book.get_by_author(db, book_author=author_name)


@router.get('/title/{title}', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_by_title(title: str = Path(min_length=3), db: Session = Depends(get_db)):
    return crud_book.get_by_title(db, book_title=title)


@router.get('/year/{year}', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_by_year(year: int = Path(gt=0), db: Session = Depends(get_db)):
    return crud_book.get_by_year(db, book_year=year)


@router.get('/available', response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_available(db: Session = Depends(get_db)):
    return crud_book.get_by_availability(db, book_availability=True)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest, db: Session = Depends(get_db),
                      current_user=Depends(get_current_admin_user)):
    crud_book.create(db, obj_request=book_request)


@router.post('/{book_id}/categories/{category_name}', status_code=status.HTTP_201_CREATED)
async def add_category_to_book(book_id: int = Path(gt=0), category_name: str = Path(min_length=3),
                               db: Session = Depends(get_db), current_user=Depends(get_current_admin_user)):
    crud_book.add_category_to_book(db, book_id=book_id, category_name=category_name)


@router.put('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest, book_id: int = Path(gt=0), db: Session = Depends(get_db),
                      current_user=Depends(get_current_admin_user)) -> None:
    crud_book.update(db, obj_id=book_id, obj_request=book_request)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0), db: Session = Depends(get_db),
                      current_user=Depends(get_current_admin_user)) -> None:
    crud_book.remove(db, obj_id=book_id)


@router.delete('/{book_id}/categories/{category_name}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_from_book(book_id: int = Path(gt=0), category_name: str = Path(min_length=3),
                                    db: Session = Depends(get_db),
                                    current_user=Depends(get_current_admin_user)) -> None:
    crud_book.delete_category_from_book(db, book_id=book_id, category_name=category_name)


@router.get('/{book_id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_by_id(book_id: int = Path(gt=0), db: Session = Depends(get_db)) -> Book:
    return crud_book.get(db, obj_id=book_id)
