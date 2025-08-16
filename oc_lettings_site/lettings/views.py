# oc_lettings_site/lettings/views.py
from django.shortcuts import render, get_object_or_404
from .models import Letting

def index(request):
    """
    Liste des locations.
    """
    lettings = Letting.objects.select_related("address").all()
    return render(request, "lettings/index.html", {"lettings_list": lettings})

def letting(request, letting_id: int):
    """
    Détail d'une location.
    """
    letting = get_object_or_404(Letting.objects.select_related("address"), pk=letting_id)
    return render(
        request,
        "lettings/letting.html",   # adapte si ton fichier s'appelle autrement
        {
            "letting": letting,           # pour {{ letting.* }}
            "address": letting.address,   # pour {{ address.* }}
            "title": letting.title,       # pour {{ title }} si utilisé
        },
    )