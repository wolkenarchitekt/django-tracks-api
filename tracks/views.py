import logging

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from tracks.models import Track
from tracks.serializers import TrackSerializer

logger = logging.getLogger(__name__)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    schema = AutoSchema()

    paginate_by = 10

    def retrieve(self, request, *args, **kwargs):
        station = get_object_or_404(Track.objects.all(), pk=kwargs['pk'])
        serializer = TrackSerializer(station)
        logger.info("Playing: {}".format(station.name))
        return Response(serializer.data)
