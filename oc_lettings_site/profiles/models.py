"""This file defines the Profile model which extends the Django User with extra fields."""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Extension of the User model with a favorite city."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Returns the username of the associated User."""
        return self.user.username
