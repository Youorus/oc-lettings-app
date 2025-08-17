from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/index.html
    return render(request, "oc_lettings_site/index.html")



def sentry_debug(request):
    division_by_zero = 1 / 0  # volontaire pour tester
    return HttpResponse("Ceci ne s’affichera jamais :)")

def custom_404(request, exception):
    """Vue personnalisée pour la page 404"""
    return render(request, "404.html", status=404)

def custom_500(request):
    """Vue personnalisée pour la page 500"""
    return render(request, "500.html", status=500)