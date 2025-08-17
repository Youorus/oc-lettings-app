from django.contrib.auth.models import User
from oc_lettings_site.profiles.models import Profile


def test_profile_str(db):
    user = User.objects.create_user(username="alice", password="x")
    profile = Profile.objects.create(user=user, favorite_city="Lyon")
    assert str(profile) == "alice"