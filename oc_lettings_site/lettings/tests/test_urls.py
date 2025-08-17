# oc_lettings_site/lettings/tests/test_urls.py
from django.urls import reverse, resolve
from oc_lettings_site.lettings import views


def test_index_url_resolves():
    url = reverse("lettings:index")
    match = resolve(url)
    assert match.func == views.index


def test_detail_url_resolves(letting):
    url = reverse("lettings:detail", kwargs={"letting_id": letting.id})
    match = resolve(url)
    assert match.func == views.letting