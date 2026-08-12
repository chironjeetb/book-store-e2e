"""Comprehensive tests for the BookStore application."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base, Book

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def setup_database():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_database):
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with overridden database dependency."""
    return TestClient(app)


class TestHealthCheck:
    """Health check endpoint tests."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestBookListAPI:
    """Tests for book listing API."""

    def test_list_books_empty(self, client):
        """Test listing books when database is empty."""
        response = client.get("/api/books")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_books_with_data(self, client, db_session):
        """Test listing books with data."""
        # Add sample books
        books = [
            Book(title="Test Book 1", author="Author 1", description="Desc 1", price=10.0),
            Book(title="Test Book 2", author="Author 2", description="Desc 2", price=20.0),
        ]
        for book in books:
            db_session.add(book)
        db_session.commit()

        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Test Book 1"


class TestBookCreationAPI:
    """Tests for book creation API."""

    def test_create_book_success(self, client):
        """Test successful book creation."""
        payload = {
            "title": "New Book",
            "author": "Test Author",
            "description": "Test Description",
            "price": 25.99,
        }
        response = client.post("/api/books", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Book"
        assert data["price"] == 25.99
        assert "id" in data

    def test_create_book_invalid_price(self, client):
        """Test book creation with invalid price."""
        payload = {
            "title": "New Book",
            "author": "Test Author",
            "description": "Test Description",
            "price": -5.0,
        }
        response = client.post("/api/books", json=payload)
        assert response.status_code == 422  # Validation error

    def test_create_book_missing_field(self, client):
        """Test book creation with missing required field."""
        payload = {
            "title": "New Book",
            "author": "Test Author",
            # Missing description
            "price": 25.99,
        }
        response = client.post("/api/books", json=payload)
        assert response.status_code == 422


class TestBookRetrievalAPI:
    """Tests for individual book retrieval."""

    def test_get_book_success(self, client, db_session):
        """Test getting a book by ID."""
        book = Book(
            title="Retrievable Book",
            author="Test Author",
            description="Test Description",
            price=15.0,
        )
        db_session.add(book)
        db_session.commit()

        response = client.get(f"/api/books/{book.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Retrievable Book"
        assert data["id"] == book.id

    def test_get_book_not_found(self, client):
        """Test getting a non-existent book."""
        response = client.get("/api/books/9999")
        assert response.status_code == 404


class TestBookUpdateAPI:
    """Tests for book update API."""

    def test_update_book_success(self, client, db_session):
        """Test updating a book."""
        book = Book(
            title="Old Title",
            author="Old Author",
            description="Old Description",
            price=10.0,
        )
        db_session.add(book)
        db_session.commit()

        payload = {"title": "New Title", "price": 20.0}
        response = client.put(f"/api/books/{book.id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["price"] == 20.0
        assert data["author"] == "Old Author"  # Unchanged

    def test_update_book_not_found(self, client):
        """Test updating a non-existent book."""
        payload = {"title": "New Title"}
        response = client.put("/api/books/9999", json=payload)
        assert response.status_code == 404


class TestBookDeletionAPI:
    """Tests for book deletion API."""

    def test_delete_book_success(self, client, db_session):
        """Test deleting a book."""
        book = Book(
            title="Deletable Book",
            author="Test Author",
            description="Test Description",
            price=10.0,
        )
        db_session.add(book)
        db_session.commit()
        book_id = book.id

        response = client.delete(f"/api/books/{book_id}")
        assert response.status_code == 204

        # Verify book is deleted
        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == 404

    def test_delete_book_not_found(self, client):
        """Test deleting a non-existent book."""
        response = client.delete("/api/books/9999")
        assert response.status_code == 404


class TestHomePage:
    """Tests for the home page view."""

    def test_home_page_renders(self, client):
        """Test home page rendering."""
        response = client.get("/")
        assert response.status_code == 200
        assert "BookStore" in response.text
        assert "Add a New Book" in response.text


@pytest.mark.unit
def test_book_model_repr(db_session):
    """Test Book model repr."""
    book = Book(
        title="Test Book",
        author="Test Author",
        description="Test Desc",
        price=10.0,
    )
    assert "<Book(" in repr(book)
    assert "Test Book" in repr(book)
