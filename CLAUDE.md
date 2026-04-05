# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Solana wallet transaction tracker API built with FastAPI + async SQLAlchemy + PostgreSQL. It tracks cryptocurrency transactions for subscribed wallet addresses, with planned Helius webhook integration for real-time updates.

## Running the Application

```bash
# Start development server (runs on 127.0.0.1:8000)
python -m src.main
```

## Database Migrations (Alembic)

```bash
# After modifying models, generate a migration
alembic revision --autogenerate -m "description"

# Apply pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Architecture

The app uses an async-first architecture throughout:

- **`src/main.py`** — Entry point; initializes settings and starts Uvicorn
- **`src/api/create_app.py`** — FastAPI factory with lifespan manager (startup: DB connectivity check via `SELECT 1`; shutdown: close connection pools)
- **`src/api/routes/`** — Route modules go here (currently empty)
- **`src/core/config.py`** — Pydantic `Settings` loaded from `.env`, accessed via `get_settings()` (cached with `lru_cache`)
- **`src/core/database.py`** — Async SQLAlchemy engine + `AsyncSession` factory; exposes `get_db()` as a FastAPI dependency
- **`src/models/models.py`** — ORM models using SQLAlchemy 2.0+ `Mapped`/`mapped_column` style
- **`alembic/env.py`** — Migration runner; pulls `DATABASE_URL` from Pydantic settings, supports async migrations

## Data Models

**`Subscription`** — Wallets being tracked (`wallet_address` unique/indexed, `is_active`, `created_at`)

**`Transaction`** — Solana transactions (`signature` unique/indexed, `wallet_address` FK→subscriptions with cascade delete, `type`, `amount` in lamports, `from_address`, `to_address`, `token_mint`, `slot`, `timestamp`, `raw_data` JSON, `created_at`)

## Environment

Requires a `.env` file with:
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/wallet-tracker
```

The asyncpg driver is required for async DB operations. Future config will include Helius API keys for Solana webhook integration.

## Key Conventions

- All database access must use `async`/`await` with `AsyncSession`
- New routes: create a module in `src/api/routes/` and register it in `create_app.py`
- Settings are always accessed via `get_settings()`, never imported directly
- SQLAlchemy models inherit from `Base` in `src/models/sqlalchemy_base.py`
