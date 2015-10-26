import json

import mock
import networkx as nx
from networkx.readwrite import json_graph

from settings import GRAPH_FILE


class MusicGraph(nx.Graph):

    def get_artist_names(self):
        return set(self.nodes())

    @classmethod
    def from_python(cls, python):
        with mock.patch.object(nx, 'Graph', cls):
            return json_graph.node_link_graph(python)

    def to_python(self):
        return json_graph.node_link_data(self)

    def to_json(self):
        return (json.dumps(self.to_python(), indent=2, sort_keys=True)
                .replace(' \n', '\n'))

    def add_nodes_from_library(self, library):
        for name, mbid in library['name2id'].items():
            self.add_node(name, mbid=mbid)

    @classmethod
    def load(cls):
        with open(GRAPH_FILE, 'r') as fp:
            graph = cls.from_python(json.load(fp))

        return graph


    def save(self):
        with open(GRAPH_FILE, 'w') as fp:
            fp.write(self.to_json())
