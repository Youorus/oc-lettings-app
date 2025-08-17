from django.urls import reverse


def test_index_view_ok(client, profile):
    url = reverse("profiles:index")
    resp = client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    # Le nom d'utilisateur doit apparaître dans la liste
    assert profile.user.username in html


def test_detail_view_ok(client, profile):
    url = reverse("profiles:detail", kwargs={"username": profile.user.username})
    resp = client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    # Quelques infos pertinentes de la page détail
    assert profile.user.username in html
    assert profile.user.email in html
    assert profile.favorite_city in html


def test_detail_view_404(client):
    url = reverse("profiles:detail", kwargs={"username": "notfound"})
    resp = client.get(url)
    assert resp.status_code == 404