import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def path(*args):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, *args)


DATABASE_SCHEMA_FILE = path('music_graph', 'db', 'schema.sql')
DATABASE_PATH = path('data', 'db.sqlite3')
DATABASE_URI = 'sqlite:///' + DATABASE_PATH
ECHONEST_SIMILAR_ARTISTS_FILE = os.path.join(BASE_DIR, 'data',
                                             'echonest_similar_artists.json')
GOOGLE_LIBRARY_FILE = os.path.join(BASE_DIR, 'data', 'google_library.json')
GRAPH_FILE = os.path.join(BASE_DIR, 'data', 'graph.json')
LIBRARY_FILE = os.path.join(BASE_DIR, 'data', 'library.json')

ECHO_SQL = bool(os.getenv('ECHO_SQL'))
