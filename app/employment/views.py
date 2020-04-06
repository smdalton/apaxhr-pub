from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class LifeCycleHome(TemplateView):
    template_name = 'lifecycle/lifecycle_home.html'