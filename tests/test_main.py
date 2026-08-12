import pytest
from fastapi.testclient import TestClient
from app.main import app, Base, engine


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_homepage_renders():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Bookstore" in response.text


def test_list_books_returns_json():
    client = TestClient(app)
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_read_book():
    client = TestClient(app)
    new_book = {
        "title": "Test Book",
        "author": "Tester",
        "description": "A book created during tests.",
        "price": 12.34,
    }
    post_resp = client.post("/books", json=new_book)
    assert post_resp.status_code == 201
    created = post_resp.json()
    assert created["title"] == new_book["title"]
    assert created["author"] == new_book["author"]

    get_resp = client.get(f"/books/{created['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == created["id"]
