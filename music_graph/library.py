from collections import Counter
from collections import defaultdict
import re
import sys

from music_graph.settings import LIBRARY_FILE
from music_graph.track import get_tracks
from music_graph.utils import Persistable
from music_graph.utils import progress


MBID_REGEX = re.compile(r'[0-9a-fA-F]' * 8 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 12)


class ValidationError(Exception):
    pass


class MusicLibrary(Persistable):
    file = LIBRARY_FILE

    def __init__(self, path=None):
        self.data = defaultdict(lambda: {'names': Counter(),
                                    'genres': Counter()})
        if path:
            self.populate(path)
        self.data = dict(self.data)

    def populate(self, path):
        for track in progress(get_tracks(path)):
            try:
                artist_name = validate_artist_name(track.artistname)
                artist_id = validate_artist_id(track.artistid)
                genre = validate_artist_genre(track.genre)
            except ValidationError:
                print("Failed to validate track: %s" % track, file=sys.stderr)
                continue
            self.data[artist_id]['names'].update([artist_name])
            self.data[artist_id]['genres'].update([genre])

    def to_python(self):
        return self.data

    @classmethod
    def from_python(cls, python):
        instance = cls()
        instance.data = python
        return instance

def validate_artist_id(artist_id):
    artist_id = str(artist_id)
    if MBID_REGEX.match(artist_id):
        return artist_id
    else:
        raise ValidationError


def validate_artist_name(artist_name):
    if artist_name:
        return str(artist_name)
    else:
        raise ValidationError


def validate_artist_genre(genre):
    return str(genre)
