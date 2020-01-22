import logging
import os
import subprocess
from pathlib import Path
from typing import List

import pytest
from django.conf import settings

logger = logging.getLogger(__name__)


def create_mp3(filename, duration=5):
    path = os.path.join(settings.MEDIA_ROOT, filename)

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
    )
    return Path(path)


@pytest.fixture(scope="session")
def mp3_file(request) -> Path:
    """ Generate a valid MP3 file using ffmpeg """
    filename = request.param
    return create_mp3(filename)


@pytest.fixture(scope="session")
def mp3_files(request) -> List[Path]:
    """ Generate multiple MP3 files """
    count = request.param
    paths = []
    for i in range(count):
        filename = f"test{i}.mp3"
        paths.append(create_mp3(filename))
    return paths
