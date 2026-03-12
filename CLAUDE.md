# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Docker (primary)
```bash
# Build and start all services (MySQL + Django)
docker-compose up --build

# Run migrations inside the container
docker-compose exec web uv run manage.py migrate

# Create a superuser
docker-compose exec web uv run manage.py createsuperuser

# Run tests
docker-compose exec web uv run manage.py test

# Run a single test
docker-compose exec web uv run manage.py test items.tests.MyTestClass.test_method
```

### Local (no Docker)
```bash
uv sync
uv run manage.py runserver
uv run manage.py migrate
uv run manage.py makemigrations
uv run manage.py check
```

## Architecture

The project uses the **Two Scoops of Django** convention: the Django project package is named `config/` (instead of the project directory name) to avoid ambiguity.

- `config/` — project-level settings, root URL conf, wsgi/asgi entry points
- `items/` — the single app; follows standard `startapp` layout

**Request flow:** `config/urls.py` → `items/urls.py` (mounted at `/api/`) → `ItemViewSet` → `ItemSerializer` → `Item` model

**API layer:** DRF `ModelViewSet` registered on a `DefaultRouter`, giving full CRUD at `/api/items/` and `/api/items/{id}/`. The DRF browsable API is available in the browser at those URLs.

**Settings:** `DJANGO_SETTINGS_MODULE` is set to `config.settings` in both `manage.py` and `config/wsgi.py`/`config/asgi.py`. The secret key and `DEBUG=True` are hardcoded development values — use environment variables before deploying.
