"""
This module defines URL patterns for the `profiles` application.
"""
from django.urls import path
from . import views

app_name = "profiles"

# List of URL patterns mapping routes to views for the profiles app.
urlpatterns = [
    path("", views.index, name="index"),  # /profiles/
    path("<str:username>/", views.profile, name="detail"),  # /profiles/john/
]
