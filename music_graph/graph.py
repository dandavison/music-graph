import mock
import networkx as nx
from networkx.readwrite import json_graph

from music_graph.settings import GRAPH_FILE
from music_graph.utils import Persistable


class MusicGraph(nx.Graph, Persistable):
    file = GRAPH_FILE

    def get_artist_names(self):
        return set(self.nodes())

    def add_nodes_from_library(self, library):
        for name, mbid in library.get_name_ids():
            self.add_node(name, mbid=mbid)

    @classmethod
    def from_python(cls, python):
        with mock.patch.object(nx, 'Graph', cls):
            return json_graph.node_link_graph(python)

    def to_python(self):
        return json_graph.node_link_data(self)
