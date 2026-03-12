# posts

A vanilla Django app for displaying blog posts using class-based views and HTML templates.

## Files

### `models.py`
Defines the `Post` model with `title`, `body`, `published_at` (optional — a null value means the post is a draft), and `created_at` (set automatically on creation).

### `views.py`
Two class-based views, both using `get_context_data` to inject extra variables into the template beyond what the base class provides by default:

- **`PostListView`** — extends `ListView`. Fetches all posts and adds `total_posts` (a count) to the template context.
- **`PostDetailView`** — extends `DetailView`. Fetches a single post by `pk` and adds `related_posts` (up to 3 other posts) to the template context.

`get_context_data` always calls `super()` first to preserve the base context (the queryset / object), then adds to it before returning.

### `urls.py`
Defines two URL patterns under the `posts` namespace, which allows templates to reverse URLs with `{% url 'posts:list' %}` and `{% url 'posts:detail' pk %}`:

| URL | View | Name |
|-----|------|------|
| `/posts/` | `PostListView` | `posts:list` |
| `/posts/{id}/` | `PostDetailView` | `posts:detail` |

### `templates/posts/`
Django resolves templates by searching each app's `templates/` directory. The double-nesting (`templates/posts/`) namespaces the templates so they don't clash with templates from other apps.

- **`post_list.html`** — renders the list of posts and displays `total_posts` from context.
- **`post_detail.html`** — renders a single post and a sidebar of `related_posts`.

### `apps.py`
App configuration. Registers the app under the name `"posts"` with `BigAutoField` as the default primary key type.

### `migrations/`
Auto-generated database migrations. Run `uv run manage.py makemigrations posts` after changing `models.py`.

### `tests.py`
Empty test file. Add `TestCase` subclasses here to test views and model behaviour.
