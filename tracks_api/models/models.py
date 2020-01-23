import logging

from django.db import models

logger = logging.getLogger(__name__)


class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True, null=True)
    artist = models.TextField(blank=True, null=True)
    album = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    bpm = models.IntegerField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)  # 1-12 + d/m
    file = models.FileField(upload_to="music")
    duration = models.FloatField(blank=True, null=True)
    file_mtime = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    bitrate = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "track"

    def __repr__(self):
        return f"Artist: {self.artist}, Title: {self.title}"


class TrackRating(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="ratings")
    email = models.EmailField()
    rating = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "track_rating"

    def __repr__(self):
        return f"Email: {self.email}, Rating: {self.rating}, Count: {self.count}"


class TrackImage(models.Model):
    image = models.ImageField(upload_to="images")
    track = models.ForeignKey("Track", on_delete=models.CASCADE, related_name="images")
    desc = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "track_image"
        managed = True

    @property
    def data(self):
        return open(self.image.file.name, "rb").read()
