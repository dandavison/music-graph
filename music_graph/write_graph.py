import os
import pickle

import networkx as nx

from settings import GRAPH_FILE


def make_graph(music_dir):
    artists = os.listdir(music_dir)

    group_fn = lambda artist: int(a[0].lower() < 'm')

    groups = {
        0: [],
        1: [],
    }
    for a in artists:
        groups[group_fn(a)].append(a)

    g = nx.Graph()
    for a1, a2 in zip(groups[0], groups[1]):
        g.add_edge(a1, a2)

    for n in g:
        g.node[n]['name'] = n

    return g


if __name__ == '__main__':
    import sys
    (music_dir,) = sys.argv[1:]
    with open(GRAPH_FILE, 'wb') as fp:
        pickle.dump(make_graph(music_dir), fp)
