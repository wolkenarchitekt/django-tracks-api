import logging

from django.db.models import Count
from django.views.generic import DetailView, ListView, UpdateView
from rest_framework import viewsets
from rest_framework.schemas import AutoSchema

from tracks_api.models import Track
from tracks_api.serializers import TrackSerializer

logger = logging.getLogger(__name__)


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.prefetch_related("images").order_by("-file_mtime")
    serializer_class = TrackSerializer
    schema = AutoSchema()


class TrackUpdateView(UpdateView):
    model = Track
    fields = []  # type: ignore


class TrackDetailView(DetailView):
    model = Track

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrackListView(ListView):
    model = Track

    def get_queryset(self):
        queryset = Track.objects.annotate(num_images=Count("images")).filter(
            num_images__gt=0
        )
        return queryset
