from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from tracks_api import views
from tracks_api.views import TrackDetailView, TrackListView, TrackUpdateView

router = routers.DefaultRouter()
router.register(r"tracks", views.TrackViewSet)

urlpatterns = [
    path("track/api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path(
        "track/detail/<int:pk>",
        TrackDetailView.as_view(),
        name="track-detail",
    ),
    path(
        "track/update/<int:pk>",
        TrackUpdateView.as_view(),
        name="track-update",
    ),
    path(
        "track/list/",
        TrackListView.as_view(),
        name="track-list",
    ),
]

# Serve static content with Django during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MUSIC_URL, document_root=settings.MUSIC_ROOT)
