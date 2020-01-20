from pathlib import Path

import pytest

from tracks_api.tracks_import import import_tracks_to_db


@pytest.mark.django_db
def test_import(mp3_file: Path):
    assert mp3_file.exists()
    import_tracks_to_db(mp3_file.parent)
