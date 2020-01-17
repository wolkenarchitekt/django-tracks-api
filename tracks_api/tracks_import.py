from django.core.files.base import ContentFile
import datetime
import logging
import os
import pathlib
from django.conf import settings

import mediafile
from tracks_api.models import Track, TrackRating, TrackImage
from tracks_api.utils import scantree, UmaskNamedTemporaryFile

logger = logging.getLogger(__name__)


def import_track(file: os.DirEntry):
    rel_file_path = os.path.relpath(file, settings.MEDIA_ROOT)
    print(file.path)

    try:
        mf = mediafile.MediaFile(file.path)
    except mediafile.FileTypeError:
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
    )
    track_was_updated = track.file_mtime and track.file_mtime < mtime_timestamp
    track.file_mtime = mtime_timestamp

    for image in mf.images:
        image_extension = image.mime_type.split('image/')[-1]
        track_image = TrackImage(track=track, desc=image.desc)
        image_file = UmaskNamedTemporaryFile(mode='wb', suffix=f'.{image_extension}')
        image_file.write(image.data)
        track_image.image.save(os.path.basename(image_file.name), ContentFile(image.data))
        track_image.save()

    if created or track_was_updated:
        for email in mf.popm.keys():
            rating, _ = TrackRating.objects.update_or_create(track=track, email=email)
            rating.rating = mf.popm[email]['rating']
            rating.count = mf.popm[email]['count']
            rating.save()

        track.file_mtime = mtime_timestamp
        track.save(update_fields=['file_mtime'])


def import_tracks(music_dir: pathlib.Path):
    files = [file for file in scantree(music_dir)]

    if not files:
        logger.warning(f"No files found in dir: {music_dir}")
    else:
        logger.info(f"Got {len(files)} files")

        for file in files:
            import_track(file)

        print(f"Found {Track.objects.count()} tracks")
