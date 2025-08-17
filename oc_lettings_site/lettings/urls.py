"""
This module defines URL patterns for the 'lettings' app.
It references views that handle the main and detail pages for lettings.
"""
from django.urls import path
from . import views

app_name = "lettings"

# URL patterns for lettings:
# - The root URL ('') routes to the index view.
# - The '<int:letting_id>/' URL routes to the letting detail view.
urlpatterns = [
    path("", views.index, name="index"),  # /lettings/
    path("<int:letting_id>/", views.letting, name="detail"),  # /lettings/1/
]
