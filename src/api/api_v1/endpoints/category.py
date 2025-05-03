from fastapi import APIRouter, Depends, Path
from starlette import status
from sqlalchemy.orm import Session
from src.api.dependecies import get_db
from src.core.auth.dependencies import get_current_admin_user
from src.crud.category import crud_category
from src.schemas.category import CategoryRequest, CategoryResponse

router = APIRouter()


@router.get('/multi',response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_multi(skip: int = 0, limit: int = 5000, db: Session = Depends(get_db)):
    return crud_category.get_multi(db, skip=skip, limit=limit)


@router.get('/name/{category_name}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_by_name(category_name: str = Path(min_length=3), db: Session = Depends(get_db)):
    return crud_category.get_by_name(db=db, category_name=category_name)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_category(category_request: CategoryRequest, db: Session = Depends(get_db),
                          current_user=Depends(get_current_admin_user)):
    return crud_category.create(db=db, obj_request=category_request)


@router.put('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_category(category_request: CategoryRequest, category_id: int = Path(gt=0),
                          db: Session = Depends(get_db), current_user=Depends(get_current_admin_user)):
    crud_category.update(db=db, obj_request=category_request, obj_id=category_id)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int = Path(gt=0), db: Session = Depends(get_db),
                          current_user=Depends(get_current_admin_user)):
    crud_category.remove(db=db, obj_id=category_id)


@router.get('/{category_id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_by_id(category_id: int = Path(gt=0), db: Session = Depends(get_db)):
    return crud_category.get(db=db, obj_id=category_id)
