"""BookStore Application - Main Entry Point."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router as books_api_router
from app.views import router as views_router

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    # Startup
    logger.info("Initializing database and loading seed data")
    init_db()
    yield
    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(
    title="BookStore API",
    description="A modern bookstore application with REST API and web UI",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routers
app.include_router(views_router, tags=["views"])
app.include_router(books_api_router, prefix="/api", tags=["api"])


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


def run() -> None:
    """Run the development server."""
    import uvicorn

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # nosec B104
