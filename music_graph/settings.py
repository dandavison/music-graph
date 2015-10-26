import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


GRAPH_FILE = os.path.join(BASE_DIR, 'data', 'graph.pickle')
LIBRARY_FILE = os.path.join(BASE_DIR, 'data', 'library.json')
