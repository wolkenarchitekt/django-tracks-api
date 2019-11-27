import logging
import os
from os import DirEntry
from typing import List

logger = logging.getLogger(__name__)


def scantree(path) -> List[DirEntry]:
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry


def import_tracks(music_dir: str):
    files = [file for file in scantree(music_dir)]

    if not files:
        logger.warning(f"No files found in dir: {music_dir}")
    else:
        logger.info(f"Got {len(files)} files")

        for file in files:
            print(file.path, file.name)
