import re

from sqlalchemy.sql import select

from music_graph.db.sqla import ENGINE
from music_graph.db.sqla import get_table
from music_graph.track import get_tracks
from music_graph.utils import warn


MBID_REGEX = re.compile(r'[0-9a-fA-F]' * 8 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 4 + '-' +
                        r'[0-9a-fA-F]' * 12)


class ValidationError(Exception):
    pass


def populate(path):
    artists = get_table('artists')
    tracks = get_table('tracks')
    conn = ENGINE.connect()

    def get_artist(artist_id, artist_name):
        query = (select([artists])
                 .where(artists.c.id == artist_id)
                 .where(artists.c.name == artist_name))
        results = conn.execute(query).fetchall()
        if results:
            [artist] = results
            return artist
        else:
            return None

    for dbm_track in get_tracks(path):
        try:
            artist_name = validate_artist_name(dbm_track.artistname)
            artist_id = validate_artist_id(dbm_track.artistid)
            genre = validate_artist_genre(dbm_track.genre)
        except ValidationError as ex:
            warn("Failed to validate track: %s (%s)" % (dbm_track.path, ex))
            continue

        artist = get_artist(artist_id, artist_name)
        if not artist:
            conn.execute(artists.insert(),
                         id=artist_id,
                         name=artist_name)
            artist = get_artist(artist_id, artist_name)

        conn.execute(tracks.insert(),
                     artist_id=artist_id,
                     name=dbm_track.trackname,
                     path=dbm_track.path,
                     genre=genre)


def validate_artist_id(artist_id):
    artist_id = str(artist_id)
    if MBID_REGEX.match(artist_id):
        return artist_id
    else:
        raise ValidationError("Invalid artist ID: %s" % artist_id)


def validate_artist_name(artist_name):
    if artist_name:
        return str(artist_name)
    else:
        raise ValidationError("Invalid artist name: %s" % artist_name)


def validate_artist_genre(genre):
    return str(genre)
