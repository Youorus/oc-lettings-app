import pytest
from django.contrib.auth.models import User
from oc_lettings_site.profiles.models import Profile


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="john",
        email="john@example.com",
        password="secret",
        first_name="John",
        last_name="Doe",
    )


@pytest.fixture
def profile(db, user):
    return Profile.objects.create(user=user, favorite_city="Paris")