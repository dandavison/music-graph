from collections import defaultdict
from collections import Counter
from collections import OrderedDict

import mock
import networkx as nx
from networkx.readwrite import json_graph
from sqlalchemy.sql import select

from music_graph.db.sqla import fetchall
from music_graph.db.sqla import get_table
from music_graph.settings import GRAPH_FILE
from music_graph.utils import Persistable


class MusicGraph(nx.Graph, Persistable):
    FILE = GRAPH_FILE

    # A networkx feature: maintain node order for consistent serialization.
    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict

    def get_artist_names(self):
        return set(self.nodes())

    def add_artist_nodes(self):
        artists_t = get_table('artists')
        tracks_t = get_table('tracks')

        genre2mbids = defaultdict(set)
        for mbid, name in fetchall(select([
                artists_t.c.id,
                artists_t.c.name])):

            # TODO: use a join rather than doing this as an additional database
            # query inside the loop
            tracks = fetchall(select([tracks_t.c.genre])
                              .where(tracks_t.c.artist_id == mbid))

            if not len(tracks) > 1:
                continue

            self.add_node(mbid, name=name)

            if tracks:
                # TODO: Use namedtuples to record which column is in which slot
                genre = Counter(t[0] for t in tracks).most_common()[0][0]
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
