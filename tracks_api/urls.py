from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from tracks_api import views

router = routers.DefaultRouter()
router.register(r"tracks", views.TrackViewSet)

urlpatterns = [path("tracks/", include(router.urls)), path("admin/", admin.site.urls)]

# Serve static content with Django during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
