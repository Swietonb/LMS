from src.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    content = Column(String(500), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    book = relationship('Book', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
