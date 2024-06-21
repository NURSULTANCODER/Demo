from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy


def index(request):
    return render(request, 'mainsite/index.html')



