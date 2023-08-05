import os

from sqlalchemy import create_engine

from .settings import db_path

_conn = None
_cursor = None
_engine = None


def get_engine(path=None):
    if path is None:
        path = os.path.abspath(db_path)
    global _engine
    if _engine is None:
        _engine = create_engine('sqlite:///%s' % (path), echo=True)
