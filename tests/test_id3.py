from faker import Faker
import pytest
from mutagen.id3 import PictureType
from tracks.utils import update_tracks_database, fpcalc_fingerprint

from tracks.id3_utils import SimpleID3, Id3Image, ID3_GEOB


def test_set_tags(mp3_file, faker: Faker):
    artist = faker.name()
    title = faker.name()
    id3 = SimpleID3(mp3_file.name)
    id3.artist = artist
    id3.title = title
    id3.save()
    id3 = SimpleID3(mp3_file.name)
    assert id3.artist == artist
    assert id3.title == title


def test_set_image(mp3_file, image_file):
    """ Test writing and reading image to MP3 file """
    image_bytes = open(image_file.name, 'rb').read()

    id3 = SimpleID3(mp3_file.name)
    id3.images = [Id3Image(desc='Cover', data=image_bytes, type=PictureType.ARTIST)]
    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert id3.images
    assert id3.images[0].desc == 'Cover'
    assert id3.images[0].type == PictureType.ARTIST


def test_set_multi_image(mp3_file, image_file):
    """ Test writing and reading multiple images to MP3 file """
    image_bytes = open(image_file.name, 'rb').read()

    id3 = SimpleID3(mp3_file.name)
    id3.images = [Id3Image(desc='Cover', data=image_bytes, type=PictureType.ARTIST),
                  Id3Image(desc='Band', data=image_bytes, type=PictureType.BAND)]

    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert len(id3.images) == 2

    assert 'Cover' in [image.desc for image in id3.images]
    assert 'Band' in [image.desc for image in id3.images]

    assert PictureType.ARTIST in [image.type for image in id3.images]
    assert PictureType.BAND in [image.type for image in id3.images]


@pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
def test_set_rating(mp3_file, rating):
    id3 = SimpleID3(mp3_file.name)
    id3.rating = rating
    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert id3.rating == rating


def test_set_bpm(mp3_file):
    id3 = SimpleID3(mp3_file.name)
    id3.bpm = 100
    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert id3.bpm == 100


def test_set_comment(mp3_file):
    comment = "test comment"
    id3 = SimpleID3(mp3_file.name)
    id3.comment = comment
    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert id3.comment == comment


def test_set_key(mp3_file):
    id3 = SimpleID3(mp3_file.name)
    id3.key = "9m"
    id3.save()

    id3 = SimpleID3(mp3_file.name)
    assert id3.key == "9m"


def test_length(mp3_file):
    id3 = SimpleID3(mp3_file.name)
    assert id3.duration


def test_set_filename(mp3_file, faker: Faker):
    filename = faker.file_name()
    id3 = SimpleID3(mp3_file.name)
    id3.filename = filename
    assert id3.filename == filename


def test_set_geob(mp3_file):
    """Test setting fingerprint and traktor ID to ID3 GEOB data frame"""
    id3 = SimpleID3(mp3_file.name)
    finger_print = fpcalc_fingerprint(mp3_file.name)
    traktor_audio_id = 'asdf123'
    id3.fingerprint = finger_print
    id3.traktor_audio_id = traktor_audio_id
    id3.save()
    assert len(id3.getall(ID3_GEOB)) == 2
    assert SimpleID3(mp3_file.name).fingerprint == finger_print
    assert SimpleID3(mp3_file.name).traktor_audio_id == traktor_audio_id
