# Getting Started

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL database (local or [Neon](https://neon.tech))

## Installation

```bash
git clone https://github.com/navaneethreddydevops/personal-finance-backend.git
cd personal-finance-backend

# Install all dependencies (including dev)
uv sync --dev
```

## Configuration

Create a `.env` file in the project root:

```env
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_SSLMODE=require

SECRET_KEY=your-secret-key-min-32-chars
```

Generate a secure `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Running the Server

```bash
# Development (with auto-reload)
uv run uvicorn app.main:app --reload

# Production
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Migrations run automatically on startup — no manual step required.

## Docker

```bash
docker build -t personal-finance-backend .
docker run -p 8000:8000 --env-file .env personal-finance-backend
```

## Development

```bash
# Lint and auto-fix
uv run ruff check --fix app/
uv run ruff format app/

# Type check
uv run mypy app

# Pre-commit (runs on every git commit automatically)
uv run pre-commit run --all-files
```

### Adding a Migration

```bash
uv run alembic revision --autogenerate -m "describe your change"
uv run alembic upgrade head
```
