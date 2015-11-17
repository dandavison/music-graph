import os
import unittest
import subprocess

from sqlalchemy import select

from music_graph.db.sqla import fetchall_flat
from music_graph.db.sqla import fetchall
from music_graph.db.sqla import get_table


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(BASE_DIR, 'tests', 'music')


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bin = Bin(os.path.join(BASE_DIR, 'bin'))
        cls.bin.create_database()

    def test_load_library(self):
        self.bin.load_library(MUSIC_DIR)
        self.assertEqual(set(get_artist_names()),
                         {'Converge', 'Will Haven'})
        self.assertEqual(len(get_tracks()), 2)

    def test_write_echonest_similar_artists(self):
        self.bin.write_echonest_similar_artists()
        self.assertEqual(
            set(map(tuple, get_similar_artist_names())),
            {('Converge', 'Will Haven'),
             ('Will Haven', 'Converge')})


def get_artist_names():
    artists_t = get_table('artists')
    return fetchall_flat(select([artists_t.c.name]))


def get_similar_artist_names():
    # TODO: Translate to sqla
    return fetchall("""
        SELECT artists_1.name, artists_2.name
        FROM similar_artists
        JOIN artists as artists_1
        ON similar_artists.artist_1_id = artists_1.id
        JOIN artists as artists_2
        ON similar_artists.artist_2_id = artists_2.id;
        """)


def get_tracks():
    tracks_t = get_table('tracks')
    return fetchall(select([tracks_t]))


class Bin(object):

    def __init__(self, path):
        self.path = path

    def dispatch(self, name, *args):
        args = ['%s/%s' % (self.path, name)] + list(args)
        subprocess.check_call(args)

    def create_database(self):
        self.dispatch('create_database')

    def load_library(self, *args):
        self.dispatch('load_library', *args)

    def write_echonest_similar_artists(self):
        self.dispatch('write_echonest_similar_artists')


if __name__ == '__main__':
    assert 'DATABASE_PATH' in os.environ
    assert 'ECHO_NEST_API_KEY' in os.environ
    unittest.main()
