import datetime
import logging
import os
import re
import subprocess
import tempfile
from os.path import isfile

import pygments
import sqlparse
from django.conf import settings
from django.db.models import Q
from django.db.utils import IntegrityError
from mutagen.id3 import ID3NoHeaderError
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import SqlLexer

from tracks.id3_utils import SimpleID3

logger = logging.getLogger(__name__)


""" World readable TemporaryFile """
def UmaskNamedTemporaryFile(*args, **kargs) -> tempfile.NamedTemporaryFile:
    fdesc = tempfile.NamedTemporaryFile(*args, **kargs)
    umask = os.umask(0)
    os.umask(umask)
    os.chmod(fdesc.name, 0o666 & ~umask)
    return fdesc


class SQLFormatter(logging.Formatter):
    """
    Format SQL and add colors (needs pygments and sqlparse)
    """
    def format(self, record):
        # Remove leading and trailing whitespaces
        sql = record.sql.strip()

        # Indent the SQL query
        sql = sqlparse.format(sql, reindent=True)

        if pygments:
            # Highlight the SQL query
            sql = pygments.highlight(
                sql,
                SqlLexer(),
                TerminalTrueColorFormatter(style='monokai')
            )

        # Set the record's statement to the formatted query
        record.statement = sql
        return super(SQLFormatter, self).format(record)


def fpcalc_fingerprint(file, mode='plain'):
    """
    Calculate fingerprint
    :param file:
    :param mode: plain|raw
    :return:
    """
    return subprocess.check_output(['fpcalc', f'-{mode}', file]).decode().strip()


def import_track(file, save_fingerprint=True):
    from tracks.models import Track

    mtime = os.path.getmtime(file.path)
    mtime_timestamp = datetime.datetime.fromtimestamp(mtime)

    track = Track.objects.filter(
        file='/' + os.path.relpath(file, settings.MEDIA_ROOT))

    if track.exists():
        track = track.get()
        if track.file_mtime == mtime_timestamp:
            logger.debug(f"File already up to date: {file.name}")
            return
    else:
        track = None

    try:
        tags = SimpleID3(file)
    except ID3NoHeaderError:
        logger.debug(f"No ID3 header: {file.name}")
        return

    if save_fingerprint and not tags.fingerprint:
        tags.fingerprint = fpcalc_fingerprint(tags.filename)
        tags.save()

    if not track:
        Track.objects.create_from_id3(tags)


def update_tracks_database(music_dir, delete_missing=False, save_fingerprint=True):
    """
    Import ID3 track data from music_dir.
    Writes track ID to comment.

    :param music_dir: music directory
    :param delete_missing: delete tracks from collection where file is missing
    :param save_fingerprint: Save fingerprint to ID3 tags
    :return:
    """
    from tracks.models import Track

    files = [file for file in os.scandir(music_dir) if isfile(file)]

    if not files:
        logger.warning(f"No files found in dir: {music_dir}")
    else:
        logger.info("Got {} files".format(len(files)))

        for file in files:
            import_track(file, save_fingerprint=save_fingerprint)

        if delete_missing:
            for track in Track.objects.all():
                if not os.path.exists(track.abspath):
                    logger.info(f"Deleting track - file is missing: {track.artist} - {track.title}")
                    track.delete()

        logger.info(f"Written {Track.objects.count()} tracks to DB")
