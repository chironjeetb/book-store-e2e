"""API routes for books management."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookRead, BookUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/books", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)) -> list[BookRead]:
    """Get all books."""
    books = db.query(Book).all()
    logger.info(f"Retrieved {len(books)} books")
    return books


@router.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> BookRead:
    """Create a new book."""
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    logger.info(f"Created book with id={db_book.id}")
    return db_book


@router.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)) -> BookRead:
    """Get a book by ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        logger.warning(f"Book with id={book_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} not found",
        )
    return book


@router.put("/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)) -> BookRead:
    """Update a book by ID."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        logger.warning(f"Book with id={book_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} not found",
        )

    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    logger.info(f"Updated book with id={book_id}")
    return db_book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a book by ID."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        logger.warning(f"Book with id={book_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id={book_id} not found",
        )

    db.delete(db_book)
    db.commit()
    logger.info(f"Deleted book with id={book_id}")
