from rest_framework import serializers
from tracks.models import Track


class TrackSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()

    class Meta:
        model = Track
        # fields = ('stationid', 'name', 'url')
        exclude = ()

    # def get_id(self, obj):
    #     return obj.track_id
