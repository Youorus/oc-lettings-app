# oc_lettings_site/lettings/tests/test_views.py
from django.urls import reverse


def test_index_view_ok(client, letting):
    url = reverse("lettings:index")
    resp = client.get(url)
    assert resp.status_code == 200
    # le template doit contenir le titre du letting listé
    assert letting.title in resp.content.decode()
    # optionnel: vérifier le template utilisé si tu veux
    # assert any(t.name.endswith("lettings/index.html") for t in resp.templates)


def test_detail_view_ok(client, letting):
    url = reverse("lettings:detail", kwargs={"letting_id": letting.id})
    resp = client.get(url)
    assert resp.status_code == 200
    html = resp.content.decode()
    # le titre et l’adresse doivent apparaître
    assert letting.title in html
    assert str(letting.address.number) in html
    assert letting.address.street in html
