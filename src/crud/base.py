from typing import Any, Generic, Type, TypeVar
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model: Type[ModelType] = model

    def get(self, db: Session, obj_id: int) -> ModelType | None:
        """
            Get an object from the database by ID.

            Parameters
            ----------
            db : Session
                SQLAlchemy database session.
            obj_id : int
                ID of the object to get. Must be a positive integer.

            Returns
            -------
            ModelType
                Retrieved database object of type ModelType or None if object does not exist.

            Raises
            ------
            HTTPException
                If object with given ID is not found (404 status code).
        """
        model: ModelType | None = db.query(self.model).filter(self.model.id == obj_id).first()
        if model is None:
            raise HTTPException(status_code=404, detail=f'Item with id {obj_id} not found.')
        return model

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 5000) -> list[ModelType]:
        return db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_request: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj_request.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, obj_id: int, obj_request: UpdateSchemaType | dict[str, Any]) -> ModelType | None:
        db_obj: ModelType | None = self.get(db, obj_id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail='Not Found!')

        if isinstance(obj_request, dict):
            update_data: dict[str, Any] = obj_request
        else:
            update_data: dict[str, Any] = obj_request.model_dump(exclude_unset=True, exclude={'category_ids'})

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, obj_id: int) -> ModelType | None:
        obj: ModelType | None = self.get(db, obj_id)
        if obj is None:
            raise HTTPException(status_code=404, detail='Not Found!')

        db.delete(obj)
        db.commit()
        return obj
