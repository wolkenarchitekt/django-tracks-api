import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List

import pytest
from django.conf import settings
from PIL import Image
from pytest_black import BlackItem
from pytest_flake8 import Flake8Item
from pytest_mypy import MypyItem

logger = logging.getLogger(__name__)


def create_mp3(path: Path, duration=5):
    subprocess.run(
        [
            "/usr/bin/ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=1000:duration={duration}",
            "-t",
            f"{duration}",
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            f"{path}",
        ],
        check=True,
        capture_output=True,
    )
    return Path(path)


@pytest.fixture(scope="session")
def image(tmpdir_factory) -> Path:
    tmpdir = tmpdir_factory.mktemp(settings.MEDIA_ROOT)
    tf = tempfile.NamedTemporaryFile(dir="/", suffix=".png")
    img = Image.new("RGB", (60, 30), color=(73, 109, 137))
    path = Path(tmpdir.join(tf.name))
    img.save(path.name)
    return path


@pytest.fixture(scope="session")
def mp3_file(request, tmpdir_factory) -> Path:
    """ Generate a valid MP3 file using ffmpeg """
    filename = request.param
    return create_mp3(path=Path(filename))


@pytest.fixture(scope="session")
def mp3_files(request, tmpdir_factory) -> List[Path]:
    """ Generate multiple MP3 files """
    count = request.param
    paths = []
    tmpdir = tmpdir_factory.mktemp("data")
    for i in range(count):
        fn = tmpdir / f"{i}.mp3"
        paths.append(create_mp3(path=fn))
    return paths


def pytest_addoption(parser):
    parser.addoption(
        "--lint-only",
        action="store_true",
        default=False,
        help="Only run linting checks",
    )


def pytest_collection_modifyitems(session, config, items):
    if config.getoption("--lint-only"):
        lint_items = []
        if config.getoption("--flake8"):
            lint_items.extend([item for item in items if type(item) == Flake8Item])
        if config.getoption("--black"):
            lint_items.extend([item for item in items if type(item) == BlackItem])
        if config.getoption("--mypy"):
            lint_items.extend([item for item in items if type(item) == MypyItem])
        items[:] = lint_items
