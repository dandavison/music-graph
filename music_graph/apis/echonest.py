import os
import sys

from pyechonest.artist import Artist
from pyechonest.catalog import create_catalog_by_name
from pyechonest.util import EchoNestAPIError

from music_graph.settings import ECHONEST_SIMILAR_ARTISTS_FILE
from music_graph.utils import Persistable
from music_graph.utils import wait_until


assert 'ECHO_NEST_API_KEY' in os.environ, \
    ("Create an echonest account and set the environment variable with "
     "`export ECHO_NEST_API_KEY=<MY_API_KEY>`")

EN_MBID_PREFIX = 'musicbrainz:artist:'
CATALOG_NAME = 'similar-artists'


class SimilarArtists(Persistable):
    FILE = ECHONEST_SIMILAR_ARTISTS_FILE
    N_SIMILAR = 100

    def __init__(self):
        self.data = {}

    def add(self, mbid):
        try:
            artist = Artist(make_echonest_mbid(mbid))
        except EchoNestAPIError as ex:
            print >>sys.stderr, ex
        else:
            self.data[mbid] = {
                'enid': artist.id,
                'similar': map(to_python, artist.get_similar(self.N_SIMILAR)),
            }

    def to_python(self):
        return self.data

    @classmethod
    def from_python(cls, python):
        instance = cls()
        instance.data = python
        return instance

    def fetch_mbids(self):
        """
        Fetch and attach MusicBrainz IDs for all similar artists.

        This is done in bulk by creating a 'catalog' (now called a 'taste
        profile') containing all similar artists, and issuing a read request
        for MBIDs against that catalog.
        """
        enids = {artist['enid'] for artist in self.all_similar_artists()}
        items = [{'item': {'artist_id': enid}} for enid in enids]

        catalog = create_catalog_by_name(CATALOG_NAME)
        ticket_id = catalog.update(items)

        def ticket_is_complete():
            return catalog.status(ticket_id)['ticket_status'] == 'complete'

        wait_until(ticket_is_complete)
        results = get_all_item_dicts(
            catalog,
            # Request additional key due to bug
            # https://developer.echonest.com/forums/thread/1090
            buckets=['id:musicbrainz', 'hotttnesss'],
            total=len(items))
        catalog.delete()
        enid2mbid = {}
        for res in results:
            try:
                [foreign] = res['foreign_ids']
            except KeyError:
                print >>sys.stderr, (
                    "Failed to get MusicBrainz ID for similar artist '%s'" %
                    res['artist_name'])
            assert foreign['catalog'] == 'musicbrainz'
            enid2mbid[res['artist_id']] = (
                extract_mbid_from_echonest_mbid(foreign['foreign_id']))

        for similar_artist in self.all_similar_artists():
            similar_artist['mbid'] = enid2mbid.get(similar_artist['enid'])

    def all_similar_artists(self):
        for mbid, artist_data in self.data.iteritems():
            for similar_artist in artist_data['similar']:
                yield similar_artist


def get_all_item_dicts(catalog, buckets, total):
    results = []
    chunk_size = 1000
    start = 0
    remaining = total
    while remaining:
        this_chunk_size = min(chunk_size, remaining)
        results.extend(catalog
                       .get_item_dicts(buckets=buckets,
                                       results=this_chunk_size,
                                       start=start))
        remaining -= this_chunk_size
        start += this_chunk_size
    return results


def to_python(artist):
    return {
        'enid': artist.id,
        'mbid': None,
        'name': artist.name,
    }


def make_echonest_mbid(mbid):
    return EN_MBID_PREFIX + mbid


def extract_mbid_from_echonest_mbid(en_mbid):
    return en_mbid.partition(EN_MBID_PREFIX)[2]
