from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Page

# Create your views here.


class PageDetailView(DetailView):
    """
    Show page content
    """
    model = Page
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'page_detail.html'


