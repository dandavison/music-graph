from music_graph.utils import round_robin


def generate_playlist(tracks, artists, artist_fn):
    """
    Generate a playlist of tracks by artists.

    tracks: list of track objects
    artists: choose playlist tracks only from artists in this set
    artist_fn: function: (track) -> artist
    """
    artist_generators = [
        (lambda artist: (t for t in tracks if artist_fn(t) == artist))(artist)
        for artist in artists
    ]
    playlist = round_robin(artist_generators)
    return list(playlist)
