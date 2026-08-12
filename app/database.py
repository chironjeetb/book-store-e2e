"""Database configuration and utilities."""

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base, Book

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./bookstore.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database and populate with seed data."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if books exist
        if db.query(Book).count() == 0:
            logger.info("Seeding database with sample books")
            seed_books = [
                Book(
                    title="Clean Code",
                    author="Robert C. Martin",
                    description="A handbook of agile software craftsmanship.",
                    price=29.99,
                ),
                Book(
                    title="The Pragmatic Programmer",
                    author="Andrew Hunt",
                    description="Journey to mastery and pragmatic development.",
                    price=34.99,
                ),
                Book(
                    title="Design Patterns",
                    author="Erich Gamma et al.",
                    description="Elements of reusable object-oriented software.",
                    price=39.99,
                ),
            ]
            db.add_all(seed_books)
            db.commit()
            logger.info("Database seeded successfully")
    finally:
        db.close()
