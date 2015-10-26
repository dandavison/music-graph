from collections import Counter
from collections import defaultdict
import json
import os
import re
import sys

from track import is_music
from track import Track


MBID_REGEX = re.compile(r'[0-9a-fA-F]' * 8 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 12)


class Library(object):
    def __init__(self, music_dir):
        self.name2ids = defaultdict(Counter)
        self.id2names = defaultdict(Counter)

        for track in progress(get_tracks(music_dir)):
            self.add_artist(track.artistname, track.artistid)

        self.name2ids = dict(self.name2ids)
        self.id2names = dict(self.id2names)

    def add_artist(self, artist_name, artist_id):
        artist_name = validate_artist_name(artist_name)
        artist_id = validate_artist_id(artist_id)
        if artist_id and artist_name:
            self.name2ids[artist_name].update([artist_id])
            self.id2names[artist_id].update([artist_name])

    def to_json(self, **kwargs):

        def _reconcile(key2counter):
            return {str(key): str(counter.most_common()[0][0])
                    for key, counter in key2counter.items()}

        return json.dumps({
            'name2id': _reconcile(self.name2ids),
            'id2name': _reconcile(self.id2names),
        }, **kwargs)


def validate_artist_id(artist_id):
    artist_id = str(artist_id)
    if MBID_REGEX.match(artist_id):
        return artist_id


def validate_artist_name(artist_name):
    if artist_name:
        return str(artist_name)


def get_tracks(music_dir):
    tracks = [Track(path)
              for path in file_paths(music_dir)
              if is_music(path)]
    for t in tracks:

        try:
            t.set_tags()
        except Exception as ex:
            print("%s: %s" % (ex.__class__.__name__, ex),
                  file=sys.stderr)
            continue

        yield t


def file_paths(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            yield os.path.join(dirpath, f)


def progress(iterable):
    for i, item in enumerate(iterable):
        yield item
        if not i % 1000:
            print(i)


if __name__ == '__main__':
    import sys
    (music_dir,) = sys.argv[1:]
    lib = Library(music_dir)
    # FIXME: settings.py
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LIBRARY_FILE = os.path.join(BASE_DIR, 'data', 'library.json')
    with open(LIBRARY_FILE, 'w') as fp:
        fp.write(lib.to_json(indent=2))
