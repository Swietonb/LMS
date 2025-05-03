from src.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.db.models.association import book_category


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    ISBN = Column(String(17), nullable=True, unique=True)
    description = Column(String(500), nullable=True)
    year = Column(Integer)
    availability = Column(Boolean, default=True, nullable=False)
    reviews = relationship('Review', back_populates='book', cascade="all, delete-orphan")
    reservations = relationship('Reservation', back_populates='book', cascade="all, delete-orphan")
    categories = relationship('Category', secondary=book_category, back_populates="books")

    @property
    def category_ids(self) -> list[int]:
        """Return list of category IDs for Pydantic compatibility"""
        return [category.id for category in self.categories]
