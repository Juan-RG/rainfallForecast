from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("help/", views.help, name='help'),
]
