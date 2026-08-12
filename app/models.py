"""Database models for BookStore application."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # type: ignore[misc]


class Book(Base):  # type: ignore[valid-type,misc]
    """Book model."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
