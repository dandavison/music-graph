import re

from music_graph.db import Table
from music_graph.settings import DATABASE_URI
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
    artist_table = Table('artist', DATABASE_URI)
    track_table = Table('track', DATABASE_URI)

    for dbm_track in get_tracks(path):
        try:
            artist_name = validate_artist_name(dbm_track.artistname)
            artist_id = validate_artist_id(dbm_track.artistid)
            genre = validate_artist_genre(dbm_track.genre)
        except ValidationError as ex:
            warn("Failed to validate track: %s (%s)" % (dbm_track.path, ex))
            continue
        artist = artist_table.select_unique_or_insert(
            id=artist_id,
            name=artist_name,
        )
        track_table.insert(
            artist_id=artist.id,
            name=dbm_track.trackname,
            path=dbm_track.path,
            genre=genre,
        )


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
