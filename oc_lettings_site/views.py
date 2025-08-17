from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/index.html
    return render(request, "oc_lettings_site/index.html")



def sentry_debug(request):
    division_by_zero = 1 / 0  # volontaire pour tester
    return HttpResponse("Ceci ne s’affichera jamais :)")