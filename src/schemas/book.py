from pydantic import BaseModel, Field


class BookRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description='Book title')
    author: str = Field(..., min_length=3, max_length=100, description='Book author')
    ISBN: str = Field(..., min_length=17, max_length=17, description='ISBN Number with (-) ')
    description: str = Field(..., min_length=3, max_length=500, description='Book description')
    year: int = Field(..., gt=1500, le=2040, description='Release date')
    availability: bool = Field(default=True, description='Availability status')
    category_ids: list[int] = Field(..., description="List of categories IDs")


class BookResponse(BookRequest):
    id: int

    model_config = {'from_attributes': True}
