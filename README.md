# django-skeleton

A minimal Django 6 + Django REST Framework skeleton with full CRUD via a REST API, backed by MySQL.

## Requirements

- Docker

## Running

```bash
docker-compose up
```

On first run, or after changing `Dockerfile` or `pyproject.toml`:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000/api/items/`.
The Django admin is at `http://localhost:8000/admin/`.

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/items/` | List all items |
| POST | `/api/items/` | Create an item |
| GET | `/api/items/{id}/` | Retrieve an item |
| PUT/PATCH | `/api/items/{id}/` | Update an item |
| DELETE | `/api/items/{id}/` | Delete an item |

## Useful commands

```bash
# Create an admin user
docker-compose exec web uv run manage.py createsuperuser

# Run tests
docker-compose exec web uv run manage.py test

# Create migrations after model changes
docker-compose exec web uv run manage.py makemigrations
```
