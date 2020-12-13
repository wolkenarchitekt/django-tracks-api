import logging
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from tracks_api.models import Track
from tracks_api.tracks_import import import_tracks_to_db

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import tracks from filesystem to database"

    def handle(self, *args, **options):
        Track.objects.all().delete()
        logging.basicConfig(level=logging.INFO)
        import_tracks_to_db(Path(settings.MUSIC_ROOT))
