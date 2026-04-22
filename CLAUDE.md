# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for all package management and command execution.

```bash
# Run the dev server
uv run uvicorn app.main:app --reload

# Lint (auto-fix) and format
uv run ruff check --fix app/
uv run ruff format app/

# Type check
uv run mypy app

# Run pre-commit on all files
uv run pre-commit run --all-files

# Add a dependency
uv add <package>
uv add --dev <package>

# Alembic migrations
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
uv run alembic downgrade -1

# Docs (MkDocs)
uv run mkdocs serve          # local preview at http://127.0.0.1:8000
uv run mkdocs build          # build static site into site/
uv run mkdocs gh-deploy      # manual deploy to GitHub Pages
```

## Architecture

FastAPI app with a layered structure: `api → services → models`, all wired through dependency injection.

**Request flow:**
1. `app/main.py` — app factory (`create_app`), mounts the v1 router, runs Alembic migrations on startup via the `lifespan` context manager.
2. `app/api/v1/router.py` — aggregates endpoint routers under `/api/v1`.
3. `app/api/v1/endpoints/` — route handlers, return Pydantic schemas.
4. `app/api/deps.py` — shared FastAPI dependencies; `get_current_user` validates the Bearer JWT and resolves the `User` ORM object.
5. `app/services/` — business logic; raises typed custom exceptions (`EmailAlreadyRegisteredError`, etc.) that endpoints catch and convert to `HTTPException`.
6. `app/models/` — SQLAlchemy ORM models inheriting from `Base` (defined in `app/core/database.py`).
7. `app/schemas/` — Pydantic request/response models. `UserResponse` uses `from_attributes = True` for ORM serialization.

**Auth:** Stateless JWT via `python-jose`. `HTTPBearer` extracts the token; `decode_access_token` returns the `user_id` (`sub` claim) or `None` on failure.

**Database:** PostgreSQL (Neon in production). SQLAlchemy engine is initialized at import time from `settings.database_url`. Migrations are auto-applied at startup — no separate migration step needed in development.

**Configuration:** `app/core/config.py` uses `pydantic-settings` to load all config from environment variables / `.env`. The `settings` singleton is module-level; required fields are `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`.

## Adding new features

- New models go in `app/models/`. Import the model in `alembic/env.py` (alongside the existing `import app.models.user`) so Alembic picks it up for `--autogenerate`.
- New endpoint groups follow the pattern: create `app/api/v1/endpoints/<name>.py`, register the router in `app/api/v1/router.py`.
- Service functions raise domain exceptions; endpoints translate them to HTTP status codes.

## Tooling

- **Ruff** (linting + formatting): configured in `pyproject.toml` under `[tool.ruff]`. `B008` is suppressed — FastAPI's `Depends()` in default args is intentional.
- **Mypy**: strict mode with the pydantic plugin. `jose` and `sqlalchemy` columns are typed with explicit `cast()` where stubs are insufficient.
- **Pre-commit**: hooks run ruff + mypy on every commit. Installed via `uv run pre-commit install`.
- **MkDocs**: docs live in `docs/`. API reference pages use `mkdocstrings` (`::: app.module` syntax). Deployed to GitHub Pages automatically on push to `master` via `.github/workflows/docs.yml`. Hosted at `https://navaneethreddydevops.github.io/personal-finance-backend/`.
