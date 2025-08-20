"""
Ce module définit les modèles principaux de l'application lettings.
Il contient :
- Address : modèle représentant une adresse postale complète.
- Letting : modèle représentant une location, associée à une adresse unique.
"""

from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models


class Address(models.Model):
    """
    Modèle représentant une adresse postale complète.
    Champs principaux :
      - number : numéro de rue
      - street : nom de la rue
      - city : ville
      - state : état (code à 2 lettres)
      - zip_code : code postal
      - country_iso_code : code ISO du pays (3 lettres)
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(
        max_length=3, validators=[MinLengthValidator(3)]
    )

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        """
        Retourne une représentation courte de l'adresse : "<numéro> <rue>".
        """
        return f"{self.number} {self.street}"


class Letting(models.Model):
    """
    Modèle représentant une location (letting).
    Chaque location possède un titre et est associée à une adresse unique via une relation OneToOne avec Address.
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Lettings"  # (facultatif mais propre)

    def __str__(self):
        """
        Retourne le titre de la location.
        """
        return self.title
