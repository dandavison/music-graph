import json

from graph import MusicGraph
from settings import GRAPH_FILE
from settings import LIBRARY_FILE


if __name__ == '__main__':
    with open(LIBRARY_FILE) as fp:
        lib = json.load(fp)
    graph = MusicGraph()
    graph.add_nodes_from_library(lib)
    with open(GRAPH_FILE, 'w') as fp:
        fp.write(graph.to_json())
