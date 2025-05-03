from fastapi import APIRouter, Depends, Path

from src.core.auth.dependencies import get_current_user, get_current_admin_user
from src.schemas.review import ReviewRequest, ReviewResponse
from src.api.dependecies import get_db
from sqlalchemy.orm import Session
from starlette import status
from src.crud.review import crud_review


router = APIRouter()


@router.get('/multi', response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_multi(skip: int = 0, limit: int = 5000, db: Session = Depends(get_db),
                    current_user=Depends(get_current_admin_user)):
    return crud_review.get_multi(db=db, skip=skip, limit=limit)


@router.get('/book/{book_id}', response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_by_book(book_id: int = Path(gt=0), db: Session = Depends(get_db),
                      current_user=Depends(get_current_admin_user)):
    return crud_review.get_by_book(db=db, book_id=book_id)


@router.get('/user/{user_id}', response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int = Path(gt=0), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_review.get_by_user(db=db, user_id=user_id, current_user=current_user)


@router.get('/rating/{rating}', response_model=list[ReviewResponse], status_code=status.HTTP_200_OK)
async def get_by_rating(rating: int = Path(gt=0, le=5), db: Session = Depends(get_db),
                        current_user=Depends(get_current_admin_user)):
    return crud_review.get_by_rating(db=db, rating=rating)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_review(review_request: ReviewRequest, db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    return crud_review.create(db=db, obj_request=review_request, current_user=current_user)


@router.put('/update/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_review(review_request: ReviewRequest, review_id: int = Path(gt=0), db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    crud_review.update(db=db, obj_id=review_id, obj_request=review_request, current_user=current_user)


@router.delete('/delete/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int = Path(gt=0), db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    crud_review.remove(db=db, obj_id=review_id, current_user=current_user)


@router.get('/{review_id}', response_model=ReviewResponse, status_code=status.HTTP_200_OK)
async def get_by_id(review_id: int = Path(gt=0), db: Session = Depends(get_db),
                    current_user=Depends(get_current_admin_user)):
    return crud_review.get(db=db, obj_id=review_id)
