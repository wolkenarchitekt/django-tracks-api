import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List

import pytest
from django.conf import settings

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
def mp3_file(request, tmpdir_factory) -> Path:
    """ Generate a valid MP3 file using ffmpeg """
    filename = request.param
    return create_mp3(path=Path(filename))


@pytest.fixture(scope="session")
def mp3_files(request, tmpdir_factory) -> List[Path]:
    """ Generate multiple MP3 files """
    tmpdir = tmpdir_factory.mktemp(settings.MEDIA_ROOT)
    count = request.param
    paths = []
    for i in range(count):
        tf = tempfile.NamedTemporaryFile(dir="/", suffix=".mp3")
        path = Path(tmpdir.join(tf.name))
        paths.append(create_mp3(path=path))
    return paths
