from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Style


class StyleListView(ListView):
    model = Style
    template_name = "styles/style_list.html"
    context_object_name = "styles"
