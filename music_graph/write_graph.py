import json

from graph import MusicGraph
from settings import GRAPH_FILE
from settings import LIBRARY_FILE


if __name__ == '__main__':
    with open(LIBRARY_FILE) as fp:
        lib = json.load(fp)
    graph = MusicGraph(lib)
    with open(GRAPH_FILE, 'w') as fp:
        json.dump(graph.to_python(), fp, indent=2)
