from src.db.base import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    return_time = Column(DateTime)
    status = Column(String(20), default="active")
    book = relationship('Book', back_populates='reservations')
    user = relationship('User', back_populates='reservations')


