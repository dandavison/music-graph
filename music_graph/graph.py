import networkx as nx
from networkx.readwrite import json_graph


class MusicGraph(nx.Graph):

    def __init__(self, library):
        super().__init__()
        for name, mbid in library['name2id'].items():
            self.add_node(name, mbid=mbid)

    @classmethod
    def from_python(cls, python):
        return json_graph.node_link_graph(python)

    def to_python(self):
        return json_graph.node_link_data(self)
