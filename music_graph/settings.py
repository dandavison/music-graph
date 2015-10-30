import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ECHONEST_SIMILAR_ARTISTS_FILE = os.path.join(BASE_DIR, 'data',
                                             'echonest_similar_artists.json')
GRAPH_FILE = os.path.join(BASE_DIR, 'data', 'graph.json')
LIBRARY_FILE = os.path.join(BASE_DIR, 'data', 'library.json')
