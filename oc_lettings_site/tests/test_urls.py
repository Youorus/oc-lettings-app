from django.urls import reverse, resolve
from oc_lettings_site import views


def test_index_url_resolves():
    url = reverse("index")
    match = resolve(url)
    assert match.func == views.index


def test_sentry_debug_url_resolves():
    url = reverse("sentry_debug")
    match = resolve(url)
    assert match.func == views.sentry_debug
