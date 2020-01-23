import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver
from tracks_api.id3_utils import update_id3

from ..entities import TrackEntity
from .models import Track

logger = logging.getLogger(__name__)


def track_model_to_entity(track: Track):
    return TrackEntity(
        artist=track.artist,
        title=track.title,
        album=track.album,
        bpm=track.bpm,
        key=track.key,
        file=track.file.path,
        duration=track.duration,
        file_mtime=track.file_mtime,
        comment=track.comment,
    )


@receiver(pre_save, sender=Track)
def update_track_receiver(sender, instance: Track, **kwargs):
    track_was_updated = "update_fields" in kwargs
    track_exists_in_db = instance.pk is not None

    if track_was_updated and track_exists_in_db:
        update_id3(track_model_to_entity(track=instance))
