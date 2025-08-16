from django.urls import path
from . import views

app_name = "lettings"

urlpatterns = [
    path("", views.index, name="index"),  # /lettings/
    path("<int:letting_id>/", views.letting, name="detail"),  # /lettings/1/
]