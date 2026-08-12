"""Views for server-rendered HTML pages."""

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate

logger = logging.getLogger(__name__)

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Create Jinja2 environment with auto-escaping
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)) -> str:
    """Render the home page with book listings."""
    try:
        books = db.query(Book).all()
        template = jinja_env.get_template("index.html")
        return template.render(request=request, books=books)
    finally:
        db.close()


@router.post("/books", response_class=RedirectResponse)
async def add_book_form(request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    """Handle book creation from web form."""
    try:
        form_data = await request.form()

        try:
            price = float(str(form_data["price"]))
        except (ValueError, KeyError) as e:
            logger.error("Invalid price provided in form")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid price format",
            ) from e

        book_data = BookCreate(
            title=str(form_data["title"]),
            author=str(form_data["author"]),
            description=str(form_data["description"]),
            price=price,
        )

        db_book = Book(**book_data.model_dump())
        db.add(db_book)
        db.commit()
        logger.info(f"Created book via form with id={db_book.id}")
    except KeyError as e:
        logger.error(f"Missing required field in form: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field: {e}",
        ) from e

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/books/{book_id}/delete", response_class=RedirectResponse)
async def delete_book_form(book_id: int, db: Session = Depends(get_db)) -> RedirectResponse:
    """Delete a book via form submission."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        logger.warning(f"Book with id={book_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    db.delete(book)
    db.commit()
    logger.info(f"Deleted book with id={book_id} via form")

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
