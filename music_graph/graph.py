from collections import defaultdict
from collections import Counter
from collections import OrderedDict
import sys

import mock
import networkx as nx
from networkx.readwrite import json_graph

from music_graph.settings import GRAPH_FILE
from music_graph.utils import Persistable


class MusicGraph(nx.Graph, Persistable):
    file = GRAPH_FILE

    # A networkx feature: maintain node order for consistent serialization.
    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict

    def get_artist_names(self):
        return set(self.nodes())

    def add_nodes_from_library(self, library):
        genre2mbids = defaultdict(set)
        for mbid, data in sorted(library.data.items()):
            if not len(data['tracks']) > 1:
                continue
            for key in ['names', 'genres']:
                if len(data[key]) > 1:
                    print("ID maps to multiple %s: %s, [%s]" %
                          (key, data[key], ', '.join(data[key])), file=sys.stderr)
            name = Counter(data['names']).most_common()[0][0]
            genre = Counter(data['genres']).most_common()[0][0]
            self.add_node(mbid, name=name, genre=genre)
            if genre:
                genre2mbids[genre].add(mbid)

        for genre, mbids in genre2mbids.items():
            mbids = sorted(mbids)
            for mbid in mbids[1:]:
                self.add_edge(mbids[0], mbid)

    @classmethod
    def from_python(cls, python):
        with mock.patch.object(nx, 'Graph', cls):
            return json_graph.node_link_graph(python)

    def to_python(self):
        return json_graph.node_link_data(self)
