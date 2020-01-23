from typing import List

from rest_framework import serializers

from tracks_api.models import Track


class TrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        exclude: List = []
