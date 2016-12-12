from django.shortcuts import render

from .forms import SearchForm
from accounts.functions import define_theme


# Create your views here.


def index_view(request):
    """
    Index view (render index.html). SHow search form. Randomize theme.
    :param request: HttpRequest
    :return: HttpResponse
    """
    form = SearchForm()
    theme_id = define_theme(request)
    return render(request, "index.html", {"theme_id": theme_id, 'form': form})


def calculator_view(request):
    """
    Calculator view. Show calculator page
    :param request: HttpRequest
    :return: HttpResponse
    """
    form = SearchForm()
    return render(request, "calculator.html", {'form': form})
