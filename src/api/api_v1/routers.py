from fastapi import APIRouter
from .endpoints import (
    book,
    category,
    reservation,
    review,
    auth,
    user
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(book.router, prefix="/books", tags=["books"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(reservation.router, prefix="/reservation", tags=["reservation"])
api_router.include_router(review.router, prefix="/review", tags=["review"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
