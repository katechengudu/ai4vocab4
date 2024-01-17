from django.views import generic
from django.urls import reverse
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')
