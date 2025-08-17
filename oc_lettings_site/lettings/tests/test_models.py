# oc_lettings_site/lettings/tests/test_models.py
from oc_lettings_site.lettings.models import Address, Letting


def test_address_str(db):
    address = Address.objects.create(
        number=42,
        street="Rue des Lilas",
        city="Paris",
        state="PA",
        zip_code=75000,
        country_iso_code="FRA",
    )
    assert str(address) == "42 Rue des Lilas"


def test_letting_str(db, letting):
    assert str(letting) == "Lovely place by the sea"