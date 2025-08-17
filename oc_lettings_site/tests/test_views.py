import pytest
from django.urls import reverse


def test_index_view_ok(client):
    url = reverse("index")
    resp = client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    # Vérifie qu’un mot clé attendu est dans le template
    assert "Welcome" in html or "Lettings" in html


def test_sentry_debug_view_raises(client):
    url = reverse("sentry_debug")
    with pytest.raises(ZeroDivisionError):
        client.get(url)


def test_custom_404_view(client):
    resp = client.get("/une-url-qui-nexiste-pas/")
    assert resp.status_code == 404
    assert "404" in resp.content.decode()


@pytest.mark.django_db
def test_custom_500_view(client, settings):
    """
    Simule une vue qui crash → handler500 doit s’exécuter.
    """
    # On force DEBUG à False pour que Django appelle handler500
    settings.DEBUG = False

    # Petite vue qui plante volontairement
    from django.urls import path
    from django.http import HttpResponse

    def crash_view(request):
        1 / 0
        return HttpResponse("jamais atteint")

    settings.ROOT_URLCONF = __name__
    urlpatterns = [path("crash/", crash_view)]

    resp = client.get("/crash/")
    assert resp.status_code == 500
    assert "500" in resp.content.decode()