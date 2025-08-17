# oc_lettings_site/tests/test_views.py
import pytest
from django.urls import reverse
from django.test import override_settings

def test_index_view_ok(client):
    url = reverse("index")
    resp = client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    assert "Welcome" in html or "Lettings" in html

def test_sentry_debug_view_raises(client):
    url = reverse("sentry_debug")
    with pytest.raises(ZeroDivisionError):
        client.get(url)

def test_custom_404_view(client, settings):
    # s'assurer que Django utilise les handlers custom
    settings.DEBUG = False
    resp = client.get("/une-url-qui-nexiste-pas/")
    assert resp.status_code == 404
    # adapte le texte au contenu de ton templates/404.html
    html = resp.content.decode().lower()
    assert "page" in html and ("introuvable" in html or "not found" in html)
