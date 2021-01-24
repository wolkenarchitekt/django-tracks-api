from typing import List
from urllib.parse import urljoin

from django.conf import settings
from rest_framework import serializers

from tracks_api.models import Track


class TrackSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_small = serializers.SerializerMethodField()
    audio = serializers.SerializerMethodField()

    def get_image(self, object: Track):
        image = object.images.first()
        if image:
            return urljoin(settings.MEDIA_ROOT, image.image.url)

    def get_image_small(self, object: Track):
        image = object.images.first()
        if image:
            return urljoin(settings.MEDIA_ROOT, image.image_small.url)

    def get_audio(self, object: Track):
        if object.file:
            return urljoin(settings.MEDIA_ROOT, object.file.url)

    class Meta:
        model = Track
        exclude: List = []
