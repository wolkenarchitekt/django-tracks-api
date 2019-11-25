import datetime
import logging
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse

from tracks.id3_utils import Id3Image, SimpleID3

logger = logging.getLogger(__name__)


class TrackManager(models.Manager):
    @staticmethod
    def create_from_id3(id3: SimpleID3):
        from tracks.utils import UmaskNamedTemporaryFile
        filename = id3.filename.replace(settings.MEDIA_ROOT, '')
        track, created = Track.objects.get_or_create(file=filename)
        track.artist = id3.artist
        track.title = id3.title
        track.rating = id3.rating
        track.bpm = id3.bpm
        track.key = id3.key
        track.duration = id3.duration
        track.comment = id3.comment
        track.finger_print = id3.fingerprint
        track.file.name = filename
        logger.debug(f"Track: {track.artist} - {track.title}")
        logger.debug(f"\tFile: {track.file.name}")
        logger.debug(f"\tURL: {track.file.url}")
        mtime = os.path.getmtime(id3.filename)
        track.file_mtime = datetime.datetime.fromtimestamp(mtime)
        track.bitrate = id3.bitrate
        track.bitrate_mode = str(id3.bitrate_mode).split('.')[1]
        track.save()

        for image in id3.images:
            if TrackImage.objects.filter(track=track, desc=image.desc).exists():
                continue
            track_image = TrackImage(track=track, desc=image.desc)
            image_file = UmaskNamedTemporaryFile(mode='wb', suffix=f'.{image.extension}')
            image_file.write(image.data)
            track_image.image.save(os.path.basename(image_file.name), ContentFile(image.data))
            logger.debug(f"\tImage URL: {track_image.image.url}")
            logger.debug(f"\tImage file: {track_image.image.file.name}")
            logger.debug(f"{track.pk}, {image.desc}")
            track_image.save()

        return track


class TrackImage(models.Model):
    image = models.ImageField(null=True, upload_to='images')
    track = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='images')
    desc = models.TextField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "track_image"
        managed = True
        unique_together = (('track', 'desc'), )

    @property
    def data(self):
        return open(self.image.file.name, 'rb').read()

    def save(self, *args, **kwargs):
        self.width = self.image.width
        self.height = self.image.height
        super().save(*args, **kwargs)


class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    artist = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    bpm = models.IntegerField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)  # 1-12 + d/m
    file = models.FileField(blank=True, null=True, upload_to='music', max_length=255, unique=True)
    duration = models.FloatField(blank=True, null=True)
    file_mtime = models.DateTimeField(null=True)  # Allows comparing timestamp when updating DB
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    bitrate = models.IntegerField(blank=True, null=True)
    bitrate_mode = models.TextField(blank=True, null=True)

    finger_print = models.TextField(blank=True, null=True)

    objects = TrackManager()

    class Meta:
        db_table = "track"
        managed = True

    def __repr__(self):
        return f"Artist: {self.artist}, Title: {self.title}"

    def get_absolute_url(self):
        return reverse("track-detail", args=[self.pk])

    @property
    def id3(self) -> SimpleID3:
        return SimpleID3(self.abspath)

    @property
    def abspath(self) -> str:
        # Fetch absolute path outside media_root
        return settings.MEDIA_ROOT + self.file.name

    def db_to_id3(self):
        # Write DB tags to ID3 tags
        id3 = self.id3

        for prop in ['artist', 'title', 'rating', 'comment']:
            id3_prop = getattr(self.id3, prop)
            db_prop = getattr(self, prop)
            if db_prop is not None and db_prop != id3_prop:
                setattr(id3, prop, db_prop)

        id3images = []
        for image in self.images.all():
            id3images.append(Id3Image(desc=image.desc, data=image.data))
        id3.images = id3images

        # Write DB images to ID3 images
        id3.save()

    def id3_to_db(self):
        # Write ID3 tags to DB tags
        from tracks.utils import UmaskNamedTemporaryFile
        id3 = self.id3

        for prop in ['artist', 'title', 'rating', 'comment']:
            id3_prop = getattr(self.id3, prop)
            db_prop = getattr(self, prop)
            if id3_prop != db_prop:
                setattr(self, prop, id3_prop)

        mtime = os.path.getmtime(id3.filename)
        self.file_mtime = datetime.datetime.fromtimestamp(mtime)
        self.save()

        TrackImage.objects.filter(track=self).delete()

        for image in id3.images:
            track_image = TrackImage(track=self, desc=image.desc)
            image_file = UmaskNamedTemporaryFile(mode='wb', suffix=f'.{image.extension}')
            image_file.write(image.data)
            track_image.image.save(os.path.basename(image_file.name), ContentFile(image.data))
            logger.debug(f"\tImage URL: {track_image.image.url}")
            logger.debug(f"\tImage file: {track_image.image.file.name}")
