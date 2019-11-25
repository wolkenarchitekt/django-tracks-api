import os
import pathlib
import tempfile
from shutil import copyfile
import names
import pytest
from django.conf import settings
from PIL import Image
from tracks.id3_utils import SimpleID3
from tracks.models import Track

FIXTURE_DIR = './tests/fixtures/'


@pytest.fixture
def mp3_file() -> tempfile.NamedTemporaryFile:
    music_dir = os.path.join(settings.MEDIA_ROOT, 'music')
    temp_file = tempfile.NamedTemporaryFile(
        mode='wb', suffix=f'.mp3', dir=music_dir, delete=False)
    copyfile(f'{FIXTURE_DIR}/sine.mp3', temp_file.name)
    return temp_file


@pytest.fixture
def image_file() -> tempfile.NamedTemporaryFile:
    temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix=f'.jpg', dir='./tests/fixtures/')
    img = Image.new('RGB', (60, 30), color='red')
    img.save(temp_file.name)
    return temp_file


@pytest.fixture
def tracks(mp3_file):
    """
    Generate mp3 files and add them to DB
    :return:
    """
    count = 5
    for i in range(0, count - 1):
        file = mp3_file
        id3 = SimpleID3(file.name)
        id3.artist = names.get_first_name()
        id3.title = names.get_last_name()
        id3.save()
        Track.objects.create_from_id3(id3)
    return Track.objects.all()


@pytest.fixture(scope='session', autouse=True)
def cleanup_files():
    yield

    music_dir = os.path.join(settings.MEDIA_ROOT, 'music')
    for p in pathlib.Path(music_dir).glob('*.mp3'):
        p.unlink()

    image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    for p in pathlib.Path(image_dir).glob('*.jpeg'):
        p.unlink()
