from more_itertools import flatten
import sqlalchemy as sqla

from music_graph import settings


_ENGINE = sqla.create_engine(settings.DATABASE_URI, echo=settings.ECHO_SQL)
_METADATA = sqla.MetaData(bind=_ENGINE)


def execute(*args, **kwargs):
    return _ENGINE.connect().execute(*args, **kwargs)


def fetchall(*args, **kwargs):
    return execute(*args, **kwargs).fetchall()


def fetchall_flat(*args, **kwargs):
    return list(flatten(fetchall(*args, **kwargs)))


def get_table(name):
    return sqla.Table(name, _METADATA, autoload=True)
