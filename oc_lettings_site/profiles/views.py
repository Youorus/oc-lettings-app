# oc_lettings_site/profiles/views.py
from django.shortcuts import render, get_object_or_404
from .models import Profile


def index(request):
    """
    Liste des profils utilisateurs.
    """
    profiles = Profile.objects.select_related("user").all()
    context = {"profiles": profiles}
    # Template: oc_lettings_site/profiles/profiles/profiles/index.html
    return render(request, "profiles/index.html", context)


def profile(request, username: str):
    """
    Détail d'un profil utilisateur via username.
    """
    profile = get_object_or_404(
        Profile.objects.select_related("user"), user__username=username
    )
    context = {"profile": profile}
    # Template: oc_lettings_site/profiles/profiles/profiles/detail.html
    return render(request, "profiles/profile.html", context)
