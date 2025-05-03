from fastapi import APIRouter, Depends, Path
from src.core.auth.dependencies import get_current_admin_user, get_current_user
from src.schemas.reservation import ReservationRequest, ReservationStatus, ReservationResponse
from starlette import status
from sqlalchemy.orm import Session
from src.api.dependecies import get_db
from src.crud.reservation import crud_reservation


router = APIRouter()


@router.get('/multi', response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
async def get_multi(skip: int = 0, limit: int = 5000, db: Session = Depends(get_db),
                    current_user=Depends(get_current_admin_user)):
    return crud_reservation.get_multi(db=db, skip=skip, limit=limit)


@router.get('/user/{user_id}', response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
async def get_by_user(user_id: int = Path(gt=0), db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    return crud_reservation.get_by_user(db=db, user_id=user_id)


@router.get('/book/{book_id}', response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
async def get_by_book(book_id: int = Path(gt=0), db: Session = Depends(get_db),
                      current_user=Depends(get_current_admin_user)):
    return crud_reservation.get_by_book(db=db, book_id=book_id)


@router.get('/status/{res_status}', response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
async def get_by_status(res_status: ReservationStatus, db: Session = Depends(get_db),
                        current_user=Depends(get_current_admin_user)):
    return crud_reservation.get_by_status(db=db, status=res_status)


@router.get('/active', response_model=list[ReservationResponse], status_code=status.HTTP_200_OK)
async def get_by_active(db: Session = Depends(get_db), current_user=Depends(get_current_admin_user)):
    return crud_reservation.get_active_reservations(db=db)


@router.get('/user/{user_id}/status/{res_status}', response_model=list[ReservationResponse],
            status_code=status.HTTP_200_OK)
async def get_by_user_and_status(res_status: ReservationStatus, user_id: int = Path(gt=0),
                                 db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_reservation.get_by_user_and_status(db=db, user_id=user_id, status=res_status)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation_request: ReservationRequest, db: Session = Depends(get_db),
                             current_user=Depends(get_current_user)):
    return crud_reservation.create(db=db, obj_request=reservation_request)


@router.put('/update/{reservation_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_reservation(reservation_request: ReservationRequest, reservation_id: int = Path(gt=0),
                             db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    crud_reservation.update(db=db, obj_id=reservation_id, obj_request=reservation_request)


@router.delete('/delete/{reservation_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: int = Path(gt=0), db: Session = Depends(get_db),
                             current_user=Depends(get_current_user)):
    crud_reservation.remove(db=db, obj_id=reservation_id)


@router.get('/{reservation_id}', response_model=ReservationResponse, status_code=status.HTTP_200_OK)
async def get_by_id(reservation_id: int = Path(gt=0), db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    return crud_reservation.get(db=db, obj_id=reservation_id)
