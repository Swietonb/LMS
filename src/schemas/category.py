from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description='Category name')


class CategoryResponse(CategoryRequest):
    id: int

    model_config = {'from_attributes': True}
