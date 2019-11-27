import logging
import os
import sys

from django.core.management.base import BaseCommand
from tracks_api.importer import import_tracks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import tracks from filesystem to database'

    def add_arguments(self, parser):
        parser.add_argument('music_dir', nargs='+', type=str)

    def handle(self, *args, **options):
        for music_dir in options['music_dir']:
            if not os.path.isdir(music_dir):
                print(f"Path not found: {music_dir}")
                sys.exit(1)

            import_tracks(music_dir)
