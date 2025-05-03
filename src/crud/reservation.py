from src.crud.base import CRUDBase
from src.db.models import Reservation
from src.schemas.reservation import ReservationRequest, ReservationStatus
from sqlalchemy.orm import Session
from typing_extensions import override
from typing import Type, Any


class CRUDReservation(CRUDBase[Reservation, ReservationRequest, ReservationRequest]):

    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[Reservation]]:
        self.validate_user(user_id=user_id, db=db)
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_book(self, db: Session, *, book_id: int) -> list[Type[Reservation]]:
        self.validate_book(book_id=book_id, db=db)
        return db.query(self.model).filter(self.model.book_id == book_id).all()

    def get_by_status(self, db: Session, *, status: ReservationStatus) -> list[Type[Reservation]]:
        return db.query(self.model).filter(self.model.status == status).all()

    def get_active_reservations(self, db: Session) -> list[Type[Reservation]]:
        return db.query(self.model).filter(self.model.status == ReservationStatus.ACTIVE).all()

    def get_by_user_and_status(self, db: Session, *, user_id: int, status: ReservationStatus)\
            -> list[Type[Reservation]]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.status == status
        ).all()

    @override
    def create(self, db: Session, *, obj_request: ReservationRequest) -> Reservation:
        self.validate_user(user_id=obj_request.user_id, db=db)
        self.validate_book(book_id=obj_request.book_id, db=db)
        return super().create(db=db, obj_request=obj_request)

    @override
    def update(self, db: Session, *, obj_id: int,
               obj_request: ReservationRequest | dict[str, Any]) -> Reservation | None:
        self.validate_user(user_id=obj_request.user_id, db=db)
        self.validate_book(book_id=obj_request.book_id, db=db)
        return super().update(db=db, obj_id=obj_id, obj_request=obj_request)


crud_reservation = CRUDReservation(Reservation)
