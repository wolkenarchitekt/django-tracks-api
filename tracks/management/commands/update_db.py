import logging
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from tracks.utils import update_tracks_database

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update tracks database from filesystem'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-missing',
            action='store_true',
            help='Delete tracks from DB where files are missing',
            default=False
        )

    def handle(self, *args, **options):
        music_dir = os.path.join(settings.MEDIA_ROOT, 'music')

        if not os.path.isdir(music_dir):
            print(f"Path not found: {music_dir}")
            sys.exit(1)

        update_tracks_database(music_dir, delete_missing=options['delete_missing'])
