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
    FILE = GRAPH_FILE

    # A networkx feature: maintain node order for consistent serialization.
    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict

    def get_artist_names(self):
        return set(self.nodes())

    def add_nodes_from_library(self, library):
        genre2mbids = defaultdict(set)
        for mbid, data in sorted(library.data.items()):
            if library.is_excluded_artist(mbid):
                continue
            if not len(data['tracks']) > 1:
                continue
            for key in ['names', 'genres']:
                if len(data[key]) > 1:
                    print >>sys.stderr, "ID maps to multiple %s: %s, [%s]" % (
                        key, data[key], ', '.join(data[key]))
            name = Counter(data['names']).most_common()[0][0]
            genre = Counter(data['genres']).most_common()[0][0]
            self.add_node(mbid, name=name, genre=genre)
            if genre:
                genre2mbids[genre].add(mbid)

        for genre, mbids in genre2mbids.items():
            self.add_node(genre, name=genre)
            for mbid in mbids:
                self.add_edge(genre, mbid)

    @classmethod
    def from_python(cls, python):
        with mock.patch.object(nx, 'Graph', cls):
            return json_graph.node_link_graph(python)

    def to_python(self):
        return json_graph.node_link_data(self)
