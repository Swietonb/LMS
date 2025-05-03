from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ReservationStatus(str, Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class ReservationRequest(BaseModel):
    book_id: int = Field(..., gt=0, description='ID of reserved book')
    user_id: int = Field(..., gt=0, description='ID of user')
    reservation_time: datetime = Field(default_factory=datetime.now,
                                       description='Time when reservation was made (auto-generated)')
    return_time: datetime = Field(..., description='Expected return time of the book')
    status: ReservationStatus = Field(default=ReservationStatus.ACTIVE,
                                      description='Status of reservation (default = active)')


class ReservationResponse(ReservationRequest):
    id: int
    model_config = {'from_attributes': True}
