"""This module configures the root URL routing for the Django project, including admin, app routes, and error handlers."""

from django.contrib import admin
from django.urls import path, include
from . import views  # si tu gardes un index global


"""Custom error handlers for 404 and 500 HTTP errors."""
handler404 = "oc_lettings_site.views.custom_404"
handler500 = "oc_lettings_site.views.custom_500"

"""Defines the URL patterns for the project."""
urlpatterns = [
    path("", views.index, name="index"),  # page d’accueil (optionnel)
    path("lettings/", include("oc_lettings_site.lettings.urls", namespace="lettings")),
    path("profiles/", include("oc_lettings_site.profiles.urls", namespace="profiles")),
    path("admin/", admin.site.urls),
    path("sentry-debug/", views.sentry_debug, name="sentry_debug"),
]
