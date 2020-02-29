import logging
import os
import tempfile
from os import DirEntry
from tempfile import _TemporaryFileWrapper  # type: ignore
from typing import Generator

logger = logging.getLogger(__name__)


def UmaskNamedTemporaryFile(*args, **kargs) -> _TemporaryFileWrapper:
    """ World readable TemporaryFile """
    fdesc = tempfile.NamedTemporaryFile(*args, **kargs)
    umask = os.umask(0)
    os.umask(umask)
    os.chmod(fdesc.name, 0o666 & ~umask)
    return fdesc


def scantree(path) -> Generator[DirEntry, None, None]:
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry
