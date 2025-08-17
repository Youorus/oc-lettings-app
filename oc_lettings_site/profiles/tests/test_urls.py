from django.urls import reverse, resolve
from oc_lettings_site.profiles import views


def test_index_url_resolves():
    url = reverse("profiles:index")
    match = resolve(url)
    assert match.func == views.index


def test_detail_url_resolves(profile):
    url = reverse("profiles:detail", kwargs={"username": profile.user.username})
    match = resolve(url)
    assert match.func == views.profile