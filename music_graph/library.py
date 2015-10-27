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


class MusicLibrary(Persistable):
    file = LIBRARY_FILE
    _attr_names = {'name2ids'}

    def __init__(self, **kwargs):
        assert kwargs.keys() == self._attr_names
        for key, val in kwargs.items():
            setattr(self, key, val)

    def to_python(self):
        return {key: getattr(self, key) for key in self._attr_names}

    @classmethod
    def from_path(cls, path):
        name2ids, defaultdict(Counter)
        for track in progress(get_tracks(path)):
            artist_name = validate_artist_name(track.artistname)
            artist_id = validate_artist_id(track.artistid)
            if artist_id and artist_name:
                name2ids[artist_name].update([artist_id])

        return cls(name2ids=dict(name2ids))

    def get_name_ids(self):
        for name, ids in self.name2ids.items():
            if len(ids) > 1:
                print("Name maps to multiple IDs: %s, [%s]" %
                      (name, ', '.join(ids)), file=sys.stderr)
            yield name, Counter(ids).most_common()[0][0]


def validate_artist_id(artist_id):
    artist_id = str(artist_id)
    if MBID_REGEX.match(artist_id):
        return artist_id


def validate_artist_name(artist_name):
    if artist_name:
        return str(artist_name)
