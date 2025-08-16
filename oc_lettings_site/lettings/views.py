# oc_lettings_site/lettings/views.py
from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """
    Liste des locations.
    """
    lettings = Letting.objects.select_related("address").all()
    context = {"lettings": lettings}
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/index.html
    return render(request, "lettings/index.html", context)


def letting(request, letting_id: int):
    """
    Détail d'une location.
    """
    letting = get_object_or_404(Letting.objects.select_related("address"), pk=letting_id)
    context = {
        "letting": letting,          # accessible dans le template
        "address": letting.address,  # alias pratique si tu veux
    }
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/letting_detail.html
    return render(request, "lettings/letting.html", context)