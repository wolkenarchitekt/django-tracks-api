from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from rest_framework import routers
from tracks_api import views

router = routers.DefaultRouter()
router.register(r"tracks", views.TrackViewSet)

urlpatterns = [
    path("tracks/", include(router.urls)),
    path("admin/", admin.site.urls),
]

# Serve with with nginx in production
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True,},
        ),
    ]
