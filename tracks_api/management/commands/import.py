import logging
import os
import sys

from django.core.management.base import BaseCommand

from tracks_api.tracks_import import import_tracks_to_db

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import tracks from filesystem to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "music-dirs", nargs="+", type=str, help="Directory containing music to scan"
        )

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        for music_dir in options["music-dirs"]:
            if not os.path.isdir(music_dir):
                logger.warning(f"Path not found: {music_dir}")
                sys.exit(1)

            import_tracks_to_db(music_dir)
