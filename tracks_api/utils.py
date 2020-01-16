import tempfile
import logging
import os
from os import DirEntry
from typing import List

logger = logging.getLogger(__name__)


""" World readable TemporaryFile """
def UmaskNamedTemporaryFile(*args, **kargs) -> tempfile.NamedTemporaryFile:
    fdesc = tempfile.NamedTemporaryFile(*args, **kargs)
    umask = os.umask(0)
    os.umask(umask)
    os.chmod(fdesc.name, 0o666 & ~umask)
    return fdesc


def scantree(path) -> List[DirEntry]:
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry
