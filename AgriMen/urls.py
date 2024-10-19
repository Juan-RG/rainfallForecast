from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('dashboard.urls')),  # Include dashboard URLs at the root

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files