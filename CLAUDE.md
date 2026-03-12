# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run dev server
uv run manage.py runserver

# Run migrations
uv run manage.py migrate

# Create migrations after model changes
uv run manage.py makemigrations

# Run all tests
uv run manage.py test

# Run tests for a specific app
uv run manage.py test items

# Run a single test
uv run manage.py test items.tests.MyTestClass.test_method

# Django system check
uv run manage.py check
```

## Architecture

The project uses the **Two Scoops of Django** convention: the Django project package is named `config/` (instead of the project directory name) to avoid ambiguity.

- `config/` — project-level settings, root URL conf, wsgi/asgi entry points
- `items/` — the single app; follows standard `startapp` layout

**Request flow:** `config/urls.py` → `items/urls.py` (mounted at `/api/`) → `ItemViewSet` → `ItemSerializer` → `Item` model

**API layer:** DRF `ModelViewSet` registered on a `DefaultRouter`, giving full CRUD at `/api/items/` and `/api/items/{id}/`. The DRF browsable API is available in the browser at those URLs.

**Settings:** `DJANGO_SETTINGS_MODULE` is set to `config.settings` in both `manage.py` and `config/wsgi.py`/`config/asgi.py`. The secret key and `DEBUG=True` are hardcoded development values — use environment variables before deploying.
