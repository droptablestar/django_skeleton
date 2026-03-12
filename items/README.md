# items

A Django REST Framework app exposing full CRUD for `Item` objects at `/api/items/`.

## Files

### `models.py`
Defines the `Item` model with three fields: `name` (required), `description` (optional), and `created_at` (set automatically on creation). This is the single source of truth for what an item looks like in the database.

### `serializers.py`
`ItemSerializer` translates `Item` model instances to and from JSON. It exposes `id`, `name`, `description`, and `created_at`. The `id` and `created_at` fields are read-only — they can't be set by the client.

### `views.py`
`ItemViewSet` wires the `Item` queryset and `ItemSerializer` together into a full set of CRUD actions (list, create, retrieve, update, partial update, destroy) by extending DRF's `ModelViewSet`. No extra code is needed — the base class handles all five operations.

### `urls.py`
Registers `ItemViewSet` on a DRF `DefaultRouter`, which automatically generates the following URL patterns:

| Method | URL | Action |
|--------|-----|--------|
| GET | `/api/items/` | list |
| POST | `/api/items/` | create |
| GET | `/api/items/{id}/` | retrieve |
| PUT / PATCH | `/api/items/{id}/` | update |
| DELETE | `/api/items/{id}/` | destroy |

### `apps.py`
App configuration. Sets `BigAutoField` as the default primary key type and registers the app under the name `"items"`.

### `migrations/`
Auto-generated database migrations. `0001_initial.py` creates the `items` table. Run `uv run manage.py makemigrations` after changing `models.py` to generate new migrations.

### `tests.py`
Empty test file. Add `TestCase` subclasses here to test the model, serializer, and API endpoints.
