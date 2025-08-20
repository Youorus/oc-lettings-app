# oc_lettings_site/lettings/tests/conftest.py
import pytest
from oc_lettings_site.lettings.models import Address, Letting


@pytest.fixture
def address(db):
    return Address.objects.create(
        number=123,
        street="Main Street",
        city="Anytown",
        state="CA",
        zip_code=90210,
        country_iso_code="USA",
    )


@pytest.fixture
def letting(db, address):
    return Letting.objects.create(
        title="Lovely place by the sea",
        address=address,
    )
