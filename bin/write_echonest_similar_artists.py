#!/usr/bin/env python
from apis.echonest import SimilarArtists
from music_graph.library import MusicLibrary
from music_graph.utils import progress


lib = MusicLibrary.load()
similar_artists = SimilarArtists()

for mbid in progress(lib.data, total=len(lib.data)):
    similar_artists.add(mbid)
    similar_artists.save()
