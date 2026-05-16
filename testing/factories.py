import datetime

import factory

from posts.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Post {n}")
    body = factory.Faker("paragraph")
    published_at = factory.Faker("date_time_this_year", tzinfo=datetime.timezone.utc)
