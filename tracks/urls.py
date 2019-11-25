from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static
from django.conf import settings

from tracks import views

router = routers.DefaultRouter()
router.register(r'tracks', views.TrackViewSet)


# Allow passwordless login to Admin
class AccessUser(object):
    has_module_perms = has_perm = __getattr__ = lambda s, *a, **kw: True


admin.site.has_permission = lambda r: setattr(r, 'user', AccessUser()) or True

schema_view = get_schema_view(title="Django Tracks")

urlpatterns = [
    path('tracks/admin/', admin.site.urls),
    path('tracks/api/', include(router.urls)),
    url('schema', schema_view),
]

# TODO: remove this when going into production / use static webserver
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
