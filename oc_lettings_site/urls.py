from django.contrib import admin
from django.urls import path, include
from . import views  # si tu gardes un index global

urlpatterns = [
    path("", views.index, name="index"),  # page d’accueil (optionnel)
    path("lettings/", include("oc_lettings_site.lettings.urls", namespace="lettings")),
    path("profiles/", include("oc_lettings_site.profiles.urls", namespace="profiles")),
    path("admin/", admin.site.urls),
]
