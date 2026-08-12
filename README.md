# End-to-End Bookstore App

A simple Python FastAPI bookstore backend with server-rendered UI, REST API, containerization, and CI/CD.

## Run locally

1. Create virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. Start the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Open http://localhost:8000

## Docker

Build and run:
```bash
docker build -t end-to-end-bookstore .
docker run --rm -p 8000:8000 end-to-end-bookstore
```

## CI/CD

GitHub Actions runs lint, tests, and builds the Docker image.
