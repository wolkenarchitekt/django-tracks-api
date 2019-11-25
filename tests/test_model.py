from django.db.models.aggregates import Count
import os
import random

from django.core.files.base import ContentFile
import pytest
from django.conf import settings
from faker import Faker

from tracks.id3_utils import Id3Image, SimpleID3
from tracks.models import Track, TrackImage
from tracks.utils import update_tracks_database, UmaskNamedTemporaryFile


@pytest.mark.django_db
def test_track_from_incomplete_id3(mp3_file):
    """ Creating track from incomplete ID3 should fail """
    id3 = SimpleID3(mp3_file.name)
    Track.objects.create_from_id3(id3)


@pytest.mark.django_db
def test_track_from_id3(mp3_file, image_file):
    """ Test import ID3 tag as track to DB """
    id3 = SimpleID3(mp3_file.name)
    id3.title = 'Title'
    id3.artist = 'Artist'
    id3.rating = 5
    id3.bpm = 123
    id3.key = '9M'
    image_bytes = open(image_file.name, 'rb').read()
    id3.images = [
        Id3Image(desc='Cover', data=image_bytes), Id3Image(desc='Cover2', data=image_bytes)]
    id3.save()

    assert len(id3.images) == 2
    assert id3.images[0].extension
    track = Track.objects.create_from_id3(id3)
    assert track.artist == 'Artist'
    assert track.title == 'Title'
    assert track.rating == 5
    assert track.bpm == 123
    assert track.key == '9M'
    assert track.images.count() == 2
    assert track.duration == id3.duration


@pytest.mark.django_db
def test_save_id3(tracks, faker: Faker):
    track = tracks[0]
    artist = faker.name()
    title = faker.name()
    rating = random.randint(1, 5)
    track.artist = artist
    track.title = title
    track.rating = rating
    track.comment = f'Test comment {random.randint(1, 10)}'
    track.save()
    track.db_to_id3()
    assert track.id3.artist == artist
    assert track.id3.title == title
    assert track.id3.rating == rating
    assert track.id3.comment == track.comment


@pytest.mark.django_db
def test_update_tracks_db(mp3_file):
    update_tracks_database(os.path.join(settings.MEDIA_ROOT, 'music'))
    track_query = Track.objects.filter(file__endswith=os.path.basename(mp3_file.name))
    assert track_query.exists()
    track = track_query.get()
    assert track
    assert track.finger_print
    assert track.id3.fingerprint


@pytest.mark.django_db
def test_save_images_to_id3(mp3_file, image_file):
    image_count = 2
    update_tracks_database(os.path.join(settings.MEDIA_ROOT, 'music'))
    track = Track.objects.annotate(image_count=Count('images')).filter(image_count=0)[0]
    image_bytes = open(image_file.name, 'rb').read()

    assert track.images.count() == 0

    for i in range(0, image_count):
        track_image = TrackImage(track=track, desc=f'image {i}')
        track_image.image.save(os.path.basename(image_file.name), ContentFile(image_bytes))

    assert track.images.count() == image_count
    track.db_to_id3()
    assert len(track.id3.images) == image_count
