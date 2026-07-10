# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency management (Python >=3.13).

```bash
uv sync                       # install dependencies into .venv
uv run python -m app.main     # run the server locally (listens on :8080)
uv add <package>              # add a dependency (updates pyproject.toml + uv.lock)
```

Docker / Compose:

```bash
docker compose up --build     # build image and run on :8080
```

There is no test suite, linter, or formatter configured in this repo yet.

## Architecture

A minimal FastAPI service that serves the Fibonacci sequence, laid out in layered packages under `app/`:

- `app/main.py` — composition root. Defines `lifespan` (startup precomputation), the `create_app()` factory (constructs `FastAPI`, includes the router, calls `add_pagination`), the module-level `app` instance, and the `main()` uvicorn entrypoint.
- `app/core/config.py` — `Settings` (pydantic-settings `BaseSettings`) exposed as the singleton `SETTINGS`. Fields default in code but are **overridden by matching OS environment variables** (e.g. `SERVER_PORT`, `SERVER_LOG_LEVEL`, `DB_URL`).
- `app/services/` — business logic, framework-agnostic. `fibonacci.py` holds `generate_fibonacci(max_value)`.
- `app/api/` — HTTP layer. `router.py` aggregates the per-resource routers under `routes/` (`root.py`, `fibonacci.py`) into `api_router`.

To add an endpoint: create/extend a router module in `app/api/routes/`, then register it in `app/api/router.py`. Keep computation in `app/services/`, not in route handlers.

Key details worth knowing before editing:

- **Startup precomputation:** the `lifespan` handler in `main.py` sets `app.state.fibonacci = generate_fibonacci(sys.maxsize)` on startup — the entire sequence up to the platform max int, cached in app state. Route handlers read it via `request.app.state.fibonacci` and never recompute. This affects startup cost and memory, not per-request work.
- **`generate_fibonacci(max_value)` semantics:** the argument is an upper *value* bound (include terms while `b <= max_value`), not a count of terms.
- **`root_path="/fibonacci/v1/"`** is set in `create_app()`. The service expects to be mounted behind a reverse proxy at that prefix. Routes are defined relative to root (`/`, `/all`); when hit directly (no proxy) docs are at `/docs`.
- **Pagination:** `/all` uses `fastapi-pagination` (`paginate()` + `add_pagination(app)`), returning a `Page[int]` with `?page=` / `?size=` query params.
- **`db_url` / Postgres:** `compose.env` and the `DB_URL` setting wire up a database, but no DB code is currently used by the app — it is scaffolding for future work.

## Deployment

- `Dockerfile` is a multi-stage build using the `uv` binary; runtime stage runs as non-root `appuser` and the entrypoint is `python -m app.main`.
- `kubernetes/` holds raw manifests (ServiceAccount, Deployment, Service) applied in numeric filename order; the Deployment pulls image `vosszen/fastapi-fibonacci-v2:latest`.
