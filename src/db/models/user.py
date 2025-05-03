from src.db.base import Base
from sqlalchemy import Column, String, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class Role(PyEnum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    reviews = relationship('Review', back_populates='user')
    reservations = relationship('Reservation', back_populates='user')
