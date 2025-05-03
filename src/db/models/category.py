from src.db.base import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.db.models.association import book_category


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", secondary=book_category, back_populates="categories")
