import os
import pytest


from tracks_api.tracks_import import import_tracks

FIXTURE_DIR = os.environ.get('FIXTURE_DIR', './tracks_api/tests/fixtures/')


@pytest.mark.django_db
def test_model():
    import_tracks(FIXTURE_DIR)

