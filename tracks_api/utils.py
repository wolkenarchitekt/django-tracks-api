import datetime
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


class SQLFormatter(logging.Formatter):
    def format(self, record):
        # Check if Pygments is available for coloring
        try:
            import pygments
            from pygments.lexers import SqlLexer
            from pygments.formatters import TerminalTrueColorFormatter
        except ImportError:
            pygments = None

        # Check if sqlparse is available for indentation
        try:
            import sqlparse
        except ImportError:
            sqlparse = None

        # Remove leading and trailing whitespaces
        sql = record.sql.strip()

        if sqlparse:
            # Indent the SQL query
            sql = sqlparse.format(sql, reindent=True)

        if pygments:
            # Highlight the SQL query
            sql = pygments.highlight(
                sql, SqlLexer(), TerminalTrueColorFormatter(style="monokai")
            )

        # Set the record's statement to the formatted query
        record.statement = sql
        return super(SQLFormatter, self).format(record)
