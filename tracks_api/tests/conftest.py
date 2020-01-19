import logging
import subprocess
import tempfile
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def mp3_file(tmp_path) -> Path:
    """ Generate a valid MP3 file using ffmpeg """
    duration = 5
    # from ipdb import set_trace; set_trace()
    # tmpdir_factory.mktemp('music').join()
    fd, path = tempfile.mkstemp(dir=tmp_path, suffix='.mp3')

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
        check=True
    )
    return Path(path)


@pytest.fixture(scope='session', autouse=True)
def cleanup_files():
    yield