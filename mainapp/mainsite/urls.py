from django.urls import path, include
from . import views

app_name = 'mainsite'

urlpatterns = [
    path('', views.index, name='home'),
]