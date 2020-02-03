import datetime
import logging
import os
import pathlib

import mediafile
from django.conf import settings
from django.core.files.base import ContentFile
from tracks_api.models import Track, TrackImage, TrackRating
from tracks_api.utils import UmaskNamedTemporaryFile, scantree

logger = logging.getLogger(__name__)


def import_track_to_db(file: os.DirEntry):
    """Import track to database using mediafile"""
    rel_file_path = os.path.relpath(file, settings.MEDIA_ROOT)

    try:
        mf = mediafile.MediaFile(file.path)
    except (mediafile.FileTypeError, mediafile.UnreadableFileError):
        logger.debug(f"Error reading tags from file '{file.path}'")
        return

    mtime = os.path.getmtime(file.path)
    mtime_timestamp = datetime.datetime.fromtimestamp(mtime)

    track, created = Track.objects.update_or_create(
        file=rel_file_path,
        artist=mf.artist,
        title=mf.title,
        comment=mf.comments,
        bpm=mf.bpm,
        key=mf.initial_key,
        duration=mf.length,
        bitrate=mf.bitrate,
        album=mf.album,
    )
    track_was_updated = track.file_mtime and track.file_mtime < mtime_timestamp
    track.file_mtime = mtime_timestamp

    for image in mf.images:
        if not image.mime_type:
            logger.error(f"Invalid mimetype: {image}")
            continue
        image_extension = image.mime_type.split("/")[-1]
        track_image = TrackImage(track=track, desc=image.desc)
        image_file = UmaskNamedTemporaryFile(mode="wb", suffix=f".{image_extension}")
        image_file.write(image.data)
        track_image.image.save(
            os.path.basename(image_file.name), ContentFile(image.data)
        )
        track_image.save()

    if created or track_was_updated:
        if mf.popm:
            for email in mf.popm.keys():
                rating, _ = TrackRating.objects.update_or_create(
                    track=track, email=email
                )
                rating.rating = mf.popm[email]["rating"]
                rating.count = mf.popm[email]["count"]
                rating.save()

            track.file_mtime = mtime_timestamp
        track.save(update_fields=["file_mtime"])


def import_tracks_to_db(music_dir: pathlib.Path):
    """Import all tracks from given path"""
    files = [file for file in scantree(music_dir)]

    if not files:
        logger.warning(f"No files found in dir: {music_dir}")
    else:
        logger.info(f"Got {len(files)} files")

        for file in files:
            import_track_to_db(file)

        logger.info(f"Found {Track.objects.count()} tracks")
