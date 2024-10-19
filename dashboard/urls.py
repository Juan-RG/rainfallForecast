from django.urls import path
from . import views  # Import views from the dashboard app

urlpatterns = [
    path("", views.home, name='home'),  # Home URL
    path("dashboard/", views.dashboard, name='dashboard'),  # Dashboard URL
    path("help/", views.help, name='help'),  # Help URL
]