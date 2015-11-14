import sqlalchemy as sqla

from music_graph.settings import DATABASE_URI


ENGINE = sqla.create_engine(DATABASE_URI)
METADATA = sqla.MetaData(bind=ENGINE)


def fetchall(*args, **kwargs):
    return ENGINE.connect().execute(*args, **kwargs).fetchall()


def get_table(name):
    return sqla.Table(name, METADATA, autoload=True)
