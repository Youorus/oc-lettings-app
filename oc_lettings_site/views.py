from django.shortcuts import render

def index(request):
    # Template d'app: oc_lettings_site/lettings/profiles/lettings/index.html
    return render(request, "index.html")

