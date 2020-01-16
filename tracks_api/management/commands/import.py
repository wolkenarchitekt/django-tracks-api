import logging
import os
import sys

from django.core.management.base import BaseCommand
from tracks_api.tracks_import import import_tracks


class Command(BaseCommand):
    help = "Import tracks from filesystem to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "music-dirs", nargs="+", type=str, help="Directory containing music to scan"
        )

    def handle(self, *args, **options):
        for music_dir in options["music-dirs"]:
            if not os.path.isdir(music_dir):
                print(f"Path not found: {music_dir}")
                sys.exit(1)

            import_tracks(music_dir)
