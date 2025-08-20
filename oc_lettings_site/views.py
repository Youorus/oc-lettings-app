"""Ce fichier définit les vues principales du projet, incluant l’index, le test Sentry,
ainsi que les gestionnaires personnalisés pour les erreurs 404 et 500."""

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """Vue d’accueil du site principal. Affiche la page d’index globale de l’application."""
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/index.html
    return render(request, "oc_lettings_site/index.html")


def sentry_debug(request):
    """Vue de test pour Sentry. Déclenche volontairement une erreur (division par zéro) afin de vérifier la journalisation des erreurs."""
    division_by_zero = 1 / 0  # volontaire pour tester
    return HttpResponse("Ceci ne s’affichera jamais :)")


def custom_404(request, exception):
    """Vue personnalisée pour gérer les erreurs 404 (Page non trouvée). Retourne un template spécifique."""
    return render(request, "404.html", status=404)


def custom_500(request):
    """Vue personnalisée pour gérer les erreurs 500 (Erreur interne du serveur). Retourne un template spécifique."""
    return render(request, "500.html", status=500)
