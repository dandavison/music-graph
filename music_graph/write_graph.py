import os
import pickle

import networkx as nx

from settings import GRAPH_FILE


def make_graph(music_dir):
    g = nx.Graph()
    g.add_nodes_from(os.listdir(music_dir))
    return g


if __name__ == '__main__':
    import sys
    (music_dir,) = sys.argv[1:]
    with open(GRAPH_FILE, 'wb') as fp:
        pickle.dump(make_graph(music_dir), fp)
