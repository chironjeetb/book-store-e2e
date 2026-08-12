# 📚 BookStore E2E Application

[![CI/CD Pipeline](https://github.com/chironjeetb/book-store-e2e/actions/workflows/ci.yml/badge.svg)](https://github.com/chironjeetb/book-store-e2e/actions)
[![codecov](https://codecov.io/gh/chironjeetb/book-store-e2e/branch/main/graph/badge.svg)](https://codecov.io/gh/chironjeetb/book-store-e2e)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, production-ready bookstore application featuring a FastAPI backend, server-rendered HTML UI, comprehensive REST API, Docker containerization, and CI/CD automation.

## 🌟 Features

### Backend
- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **SQLAlchemy ORM**: Type-safe database interactions
- **Pydantic**: Data validation and serialization
- **CORS Support**: Cross-origin requests enabled
- **Health Check Endpoint**: `/health` for monitoring

### Frontend
- **Server-Rendered HTML**: Jinja2 templates with no external JS framework
- **Responsive Design**: Mobile-first CSS with grid layout
- **Real-time Search**: Client-side book filtering
- **Modern UI**: Gradient backgrounds, smooth transitions, emoji icons

### API Endpoints
- `GET /` - Home page with all books
- `GET /api/books` - List all books (JSON)
- `POST /api/books` - Create a new book
- `GET /api/books/{id}` - Get book details
- `PUT /api/books/{id}` - Update a book
- `DELETE /api/books/{id}` - Delete a book
- `POST /books` - Create book via HTML form
- `GET /books/{id}/delete` - Delete book via HTML form
- `GET /health` - Health check

### Testing & Quality
- **Pytest**: Comprehensive test suite with 25+ tests
- **Code Coverage**: 95%+ coverage with HTML reports
- **Linting**: Ruff for fast Python linting
- **Type Checking**: MyPy for static type analysis
- **Security Scanning**: Bandit and pip-audit for vulnerability detection
- **Code Formatting**: Black and isort for consistent style

### DevOps
- **Docker**: Multi-stage build for optimized images
- **GitHub Actions**: Full CI/CD pipeline
  - Linting & formatting checks
  - Type checking
  - Security scanning
  - Automated testing with coverage
  - Docker image building & publishing
- **Health Checks**: Built-in container health monitoring

## 📋 Project Structure

```
book-store-e2e/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── routes.py            # API routes
│   ├── views.py             # HTML view routes
│   ├── static/
│   │   └── styles.css       # Responsive CSS
│   └── templates/
│       └── index.html       # Home page template
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline configuration
├── Dockerfile               # Multi-stage production build
├── .dockerignore             # Docker ignore patterns
├── .gitignore               # Git ignore patterns
├── pyproject.toml           # Project config & dependencies
├── requirements.txt         # Direct pip requirements
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Docker (optional)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/chironjeetb/book-store-e2e.git
   cd book-store-e2e
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run development server**
   ```bash
   python -m app.main
   ```
   
   Or use the convenience command:
   ```bash
   start
   ```

5. **Access the application**
   - Web UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Testing

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

### Code Quality

```bash
# Lint code
ruff check app tests

# Format code
black app tests
isort app tests

# Type checking
mypy app

# Security audit
bandit -r app
pip-audit
```

## 🐳 Docker

### Build Image
```bash
docker build -t book-store-e2e:latest .
```

### Run Container
```bash
docker run -d \
  --name bookstore \
  -p 8000:8000 \
  book-store-e2e:latest
```

### Verify Health
```bash
curl http://localhost:8000/health
```

## 📊 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Linting** - Checks code style and formatting
2. **Type Checking** - Validates type annotations
3. **Security** - Scans for vulnerabilities
4. **Testing** - Runs full test suite with coverage
5. **Building** - Creates and publishes Docker image

Triggered on:
- Push to `main` or `develop` branches
- Pull requests against `main` or `develop`

## 📈 Code Coverage

Current coverage: **95%+**

- **Unit Tests**: 20+ tests covering all endpoints
- **Integration Tests**: Form submission and database operations
- **Edge Cases**: Invalid inputs, missing resources, etc.

## 🔒 Security

- No known vulnerabilities (pip-audit)
- Code analysis with Bandit
- Type-safe code with MyPy
- Input validation with Pydantic
- Non-root Docker user
- CORS properly configured

## 📝 API Examples

### Get all books
```bash
curl http://localhost:8000/api/books
```

### Create a book
```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Clean Coder",
    "author": "Robert C. Martin",
    "description": "Professional guide to software craftsmanship",
    "price": 34.99
  }'
```

### Update a book
```bash
curl -X PUT http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 29.99}'
```

### Delete a book
```bash
curl -X DELETE http://localhost:8000/api/books/1
```

## 📚 Dependencies

### Core
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `jinja2` - Template engine

### Development
- `pytest` - Testing
- `ruff` - Linting
- `black` - Code formatting
- `mypy` - Type checking
- `bandit` - Security scanning
- `pip-audit` - Dependency auditing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`pytest && ruff check app`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust ORM
- The Python community for amazing tools

---

**Built with ❤️ for modern Python web development**
