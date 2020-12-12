from pathlib import Path
from typing import List

import pytest
from tracks_api.models import Track
from tracks_api.tracks_import import import_tracks_to_db


@pytest.mark.django_db
@pytest.mark.parametrize("mp3_files", (10,), indirect=True)
def test_import_many_files(mp3_files: List[Path]):
    import_tracks_to_db(music_dir=mp3_files[0].parent)
    assert Track.objects.count() >= 10
