import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(*args):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, *args)


def read_path(string):
    return os.path.abspath(string)


DATABASE_PATH = os.path.abspath(os.getenv('DATABASE_PATH',
                                          path('data', 'db.sqlite3')))
ECHO_SQL = bool(os.getenv('ECHO_SQL'))

DATABASE_URI = 'sqlite:///' + DATABASE_PATH

DATABASE_SCHEMA_FILE = path('music_graph', 'db', 'schema.sql')
GRAPH_FILE = os.path.join(BASE_DIR, 'data', 'graph.json')



