# Personal Finance API

A REST API for personal finance management built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Features

- JWT-based authentication (register, login, logout)
- Bearer token authorization via `HTTPBearer`
- PostgreSQL with automatic Alembic migrations on startup
- Pydantic v2 request/response validation

## Quick Start

```bash
# Install dependencies
uv sync

# Copy and fill in environment variables
cp .env.example .env

# Run the development server
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs (Swagger UI) are at `http://localhost:8000/api/docs`.

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DB_HOST` | PostgreSQL host | — |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | — |
| `DB_USER` | Database user | — |
| `DB_PASSWORD` | Database password | — |
| `DB_SSLMODE` | SSL mode | `require` |
| `SECRET_KEY` | JWT signing key | — |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL in minutes | `1440` |
