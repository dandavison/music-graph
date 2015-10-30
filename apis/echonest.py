import os
import sys

from pyechonest.artist import Artist
from pyechonest.util import EchoNestAPIError

from music_graph.settings import ECHONEST_SIMILAR_ARTISTS_FILE
from music_graph.utils import Persistable


assert 'ECHO_NEST_API_KEY' in os.environ, \
    ("Create an echonest account and set the environment variable with "
     "`export ECHO_NEST_API_KEY=<MY_API_KEY>`")


class SimilarArtists(Persistable):
    file = ECHONEST_SIMILAR_ARTISTS_FILE
    N_SIMILAR = 100

    def __init__(self):
        self.data = {}

    def add(self, mbid):
        try:
            artist = Artist("musicbrainz:artist:%s" % mbid)
        except EchoNestAPIError as ex:
            print >>sys.stderr, ex
        else:
            self.data[mbid] = {
                'enid': artist.id,
                'similar': map(to_python, artist.get_similar(self.N_SIMILAR)),
            }

    def to_python(self):
        return self.data


def to_python(artist):
    return {
        'enid': artist.id,
        'mbid': get_mbid(artist),
        'name': artist.name,
    }


# Cache MBIDs to limit queries
try:
    similar_artists = SimilarArtists.load()
except (IOError, ValueError, TypeError):
    ENID_2_MBID = {}
else:
    for mbid, data in similar_artists.data.iteritems():
        ENID_2_MBID[data['enid']] = mbid
        ENID_2_MBID.update((a['enid'], a['mbid'])
                           for a in data['similar'])

def get_mbid(artist):
    return ENID_2_MBID.get(artist.id)
