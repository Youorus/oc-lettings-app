# oc_lettings_site/profiles/views.py
# oc_lettings_site/profiles/views.py
"""
This module contains the views for the profiles app.
It provides views to list all user profiles and display details
for an individual user profile.
"""
from django.shortcuts import render, get_object_or_404
from .models import Profile


def index(request):
    """
    Displays a list of user profiles and renders the profiles index template.
    """
    profiles = Profile.objects.select_related("user").all()
    context = {"profiles": profiles}
    # Template: oc_lettings_site/profiles/profiles/profiles/index.html
    return render(request, "profiles/index.html", context)


def profile(request, username: str):
    """
    Shows the details of a user profile identified by their username,
    and renders the profile detail template.
    """
    profile = get_object_or_404(
        Profile.objects.select_related("user"), user__username=username
    )
    context = {"profile": profile}
    # Template: oc_lettings_site/profiles/profiles/profiles/detail.html
    return render(request, "profiles/profile.html", context)
