import datetime

from django.test import TestCase
from django.urls import reverse

from testing.factories import PostFactory


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class PostModelTests(TestCase):
    def test_str(self):
        post = PostFactory.build(title="Hello World")
        self.assertEqual(str(post), "Hello World")

    def test_draft_has_null_published_at(self):
        post = PostFactory(published_at=None)
        post.refresh_from_db()
        self.assertIsNone(post.published_at)

    def test_created_at_auto_set(self):
        post = PostFactory()
        post.refresh_from_db()
        self.assertIsNotNone(post.created_at)


# ---------------------------------------------------------------------------
# URL tests
# ---------------------------------------------------------------------------

class PostURLTests(TestCase):
    def test_list_url_resolves(self):
        self.assertEqual(reverse("posts:list"), "/posts/")

    def test_detail_url_resolves(self):
        post = PostFactory()
        self.assertEqual(reverse("posts:detail", args=[post.pk]), f"/posts/{post.pk}/")


# ---------------------------------------------------------------------------
# PostListView tests
# ---------------------------------------------------------------------------

class PostListViewTests(TestCase):
    def test_empty_list(self):
        response = self.client.get(reverse("posts:list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["posts"], [])
        self.assertContains(response, "No posts yet.")

    def test_posts_appear(self):
        post1 = PostFactory(title="First Post")
        post2 = PostFactory(title="Second Post")
        response = self.client.get(reverse("posts:list"))
        self.assertContains(response, post1.title)
        self.assertContains(response, post2.title)

    def test_total_posts_count(self):
        PostFactory.create_batch(3)
        response = self.client.get(reverse("posts:list"))
        self.assertEqual(response.context["total_posts"], 3)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("posts:list"))
        self.assertTemplateUsed(response, "posts/post_list.html")

    def test_post_link_to_detail(self):
        post = PostFactory()
        response = self.client.get(reverse("posts:list"))
        self.assertContains(response, reverse("posts:detail", args=[post.pk]))


# ---------------------------------------------------------------------------
# PostDetailView tests
# ---------------------------------------------------------------------------

class PostDetailViewTests(TestCase):
    def test_renders_post(self):
        post = PostFactory(title="My Title", body="My body text.")
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Title")
        self.assertContains(response, "My body text.")

    def test_404_on_invalid_pk(self):
        response = self.client.get(reverse("posts:detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_related_posts_excludes_current(self):
        post = PostFactory()
        PostFactory.create_batch(2)
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        related = list(response.context["related_posts"])
        self.assertNotIn(post, related)

    def test_related_posts_capped_at_3(self):
        post = PostFactory()
        PostFactory.create_batch(5)
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        self.assertLessEqual(len(response.context["related_posts"]), 3)

    def test_uses_correct_template(self):
        post = PostFactory()
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        self.assertTemplateUsed(response, "posts/post_detail.html")

    def test_published_at_shown(self):
        post = PostFactory(
            published_at=datetime.datetime(2025, 6, 15, tzinfo=datetime.timezone.utc)
        )
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        self.assertContains(response, "June 15, 2025")

    def test_published_at_hidden(self):
        post = PostFactory(published_at=None)
        response = self.client.get(reverse("posts:detail", args=[post.pk]))
        self.assertNotContains(response, "Published")
