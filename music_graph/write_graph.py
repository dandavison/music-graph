import json
import pickle

import networkx as nx

from settings import GRAPH_FILE
from settings import LIBRARY_FILE


def make_graph(library):
    g = nx.Graph()
    for name, mbid in library['name2id'].items():
        g.add_node(name, mbid=mbid)
    return g


if __name__ == '__main__':
    with open(LIBRARY_FILE) as fp:
        lib = json.load(fp)
    with open(GRAPH_FILE, 'wb') as fp:
        pickle.dump(make_graph(lib), fp)
