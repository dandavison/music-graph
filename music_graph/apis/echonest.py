import os
import sys

from pyechonest.artist import Artist
from pyechonest.catalog import create_catalog_by_name
from pyechonest.catalog import get_catalog_by_name
from pyechonest.util import EchoNestAPIError

from music_graph.utils import progress
from music_graph.utils import rate_limit
from music_graph.utils import repeat_until_success
from music_graph.utils import wait_until
from music_graph.utils import warn


assert 'ECHO_NEST_API_KEY' in os.environ, \
    ("Create an echonest account and set the environment variable with "
     "`export ECHO_NEST_API_KEY=<MY_API_KEY>`")

EN_MBID_PREFIX = 'musicbrainz:artist:'
CATALOG_NAME = 'similar-artists'
N_SIMILAR = 100


def fetch_similar_artists(mbids):
    similar_artists = []
    for mbid in rate_limit(progress(mbids, len(mbids)), 0.8):
        try:
            artist = Artist(make_echonest_mbid(mbid))
        except EchoNestAPIError as ex:
            warn(ex)
        else:
            similar_artists_raw = (
                repeat_until_success(lambda: artist.get_similar(N_SIMILAR),
                                     30))
            similar_artists.extend({
                'artist_1_id': mbid,
                'artist_2_enid': sim_artist.id,
            } for sim_artist in similar_artists_raw)

    enid2mbid = fetch_mbids({a['artist_2_enid'] for a in similar_artists})

    similar_artists_with_mbids = []
    for a in similar_artists:
        try:
            similar_artists_with_mbids.append({
                'artist_1_id': mbid,
                'artist_2_id': enid2mbid[a['artist_2_enid']],
            })
        except KeyError:
            pass

    return similar_artists_with_mbids


def fetch_mbids(enids):
    """
    Fetch MusicBrainz IDs for artists.

    This is done in bulk by creating a 'catalog' (now called a 'taste
    profile') containing all similar artists, and issuing a read request
    for MBIDs against that catalog.
    """
    items = [{'item': {'artist_id': enid}} for enid in set(enids)]

    def ticket_is_complete():
        return catalog.status(ticket_id)['ticket_status'] == 'complete'

    try:
        get_catalog_by_name(CATALOG_NAME).delete()
    except:
        pass

    try:
        catalog = create_catalog_by_name(CATALOG_NAME)
        ticket_id = catalog.update(items)
        wait_until(ticket_is_complete)
        results = get_all_item_dicts(catalog,
                                     # Request additional key due to bug
                                     # https://developer.echonest.com/forums/thread/1090
                                     buckets=['id:musicbrainz', 'hotttnesss'],
                                     total=len(items))
    finally:
        catalog.delete()

    enid2mbid = {}
    for res in results:
        try:
            [foreign] = res['foreign_ids']
        except KeyError:
            print >>sys.stderr, (
                "Failed to get MusicBrainz ID for similar artist '%s'" %
                res['artist_name'])
            continue
        assert foreign['catalog'] == 'musicbrainz'
        enid2mbid[res['artist_id']] = (
            extract_mbid_from_echonest_mbid(foreign['foreign_id']))

    return enid2mbid


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


def make_echonest_mbid(mbid):
    return EN_MBID_PREFIX + mbid


def extract_mbid_from_echonest_mbid(en_mbid):
    return en_mbid.partition(EN_MBID_PREFIX)[2]
