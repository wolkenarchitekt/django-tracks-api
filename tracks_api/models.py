from django.db import models


class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    artist = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
