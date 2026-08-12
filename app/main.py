from pathlib import Path

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from typing import List

DATABASE_URL = "sqlite:///./bookstore.db"
PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    cache_size=0,
)

app = FastAPI(title="Bookstore", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: float

class BookRead(BookCreate):
    id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        count = db.query(Book).count()
        if count == 0:
            db.add_all([
                Book(title="Clean Code", author="Robert C. Martin", description="A handbook of agile software craftsmanship.", price=29.99),
                Book(title="The Pragmatic Programmer", author="Andrew Hunt", description="Journey to mastery and pragmatic development.", price=34.99),
                Book(title="Design Patterns", author="Erich Gamma et al.", description="Elements of reusable object-oriented software.", price=39.99),
            ])
            db.commit()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db=Depends(get_db)):
    books = db.execute(select(Book)).scalars().all()
    template = jinja_env.get_template("index.html")
    return HTMLResponse(template.render(request=request, books=books))


@app.get("/books", response_model=List[BookRead])
def list_books(db=Depends(get_db)):
    books = db.execute(select(Book)).scalars().all()
    return books


@app.post("/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db=Depends(get_db)):
    book = Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db=Depends(get_db)):
    try:
        book = db.execute(select(Book).where(Book.id == book_id)).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/add", response_class=RedirectResponse)
async def add_book(request: Request, db=Depends(get_db)):
    form = await request.form()
    book_data = BookCreate(
        title=form["title"],
        author=form["author"],
        description=form["description"],
        price=float(form["price"]),
    )
    book = Book(**book_data.dict())
    db.add(book)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


def run():
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
