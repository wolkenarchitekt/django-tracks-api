import pytest

from tracks_api.models import Track


@pytest.mark.django_db
def test_model():
    track = Track(artist='Foo', title='Bar')
    track.save()
    assert Track.objects.count() == 1
