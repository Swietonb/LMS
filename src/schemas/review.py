from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    rating: int = Field(..., gt=0, lt=6, description='Book rating 1-5')
    content: str = Field(..., min_length=3, max_length=500, description='Review content (max 500 characters)')
    book_id: int = Field(..., gt=0, description='ID of reviewed book')
    user_id: int = Field(..., gt=0, description='ID of reviewer')


class ReviewResponse(ReviewRequest):
    id: int
    model_config = {'from_attributes': True}
