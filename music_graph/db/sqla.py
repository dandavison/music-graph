import sqlalchemy as sqla

from music_graph.settings import DATABASE_URI


_ENGINE = sqla.create_engine(DATABASE_URI)
_METADATA = sqla.MetaData(bind=_ENGINE)


def execute(*args, **kwargs):
    return _ENGINE.connect().execute(*args, **kwargs)


def fetchall(*args, **kwargs):
    return execute(*args, **kwargs).fetchall()


def get_table(name):
    return sqla.Table(name, _METADATA, autoload=True)
