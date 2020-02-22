import logging

from rest_framework import viewsets
from rest_framework.schemas import AutoSchema
from tracks_api.models import Track
from tracks_api.serializers import TrackSerializer

logger = logging.getLogger(__name__)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.prefetch_related("images").order_by("-file_mtime")
    serializer_class = TrackSerializer
    schema = AutoSchema()
