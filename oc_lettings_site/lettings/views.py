# oc_lettings_site/lettings/views.py
from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """
    Display a list of all lettings.

    This view retrieves all Letting instances, including their related addresses,
    and renders them in the 'lettings/index.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML page displaying the list of lettings.

    Context:
        lettings_list (QuerySet of Letting): List of all letting objects, each with its related address.
    """
    lettings = Letting.objects.select_related("address").all()
    return render(request, "lettings/index.html", {"lettings_list": lettings})


def letting(request, letting_id: int):
    """
    Display the details of a specific letting.

    This view fetches a Letting instance by its primary key, including its related address,
    and renders its details in the 'lettings/letting.html' template.

    Args:
        request (HttpRequest): The HTTP request object.
        letting_id (int): The primary key of the letting to display.

    Returns:
        HttpResponse: The rendered HTML page showing the letting's details.

    Context:
        letting (Letting): The letting object being displayed.
        address (Address): The address object related to the letting.
        title (str): The title of the letting.
    """
    letting = get_object_or_404(
        Letting.objects.select_related("address"), pk=letting_id
    )
    return render(
        request,
        "lettings/letting.html",
        {
            "letting": letting,
            "address": letting.address,
            "title": letting.title,
        },
    )
