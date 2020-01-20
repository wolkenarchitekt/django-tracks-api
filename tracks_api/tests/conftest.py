import logging
import os
import subprocess
from pathlib import Path

import pytest
from django.conf import settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mp3_file() -> Path:
    """ Generate a valid MP3 file using ffmpeg """
    duration = 5
    path = os.path.join(settings.MEDIA_ROOT, "test.mp3")

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


@pytest.fixture(scope="session", autouse=True)
def cleanup_files():
    yield
