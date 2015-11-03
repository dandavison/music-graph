#!/usr/bin/env python
from music_graph.db import Table
from music_graph.settings import DATABASE_URI
from music_graph.apis.echonest import fetch_similar_artists


artist_table = Table('artist', DATABASE_URI)
similar_artist_table = Table('similar_artist', DATABASE_URI)

mbids = [a.id for a in artist_table.select()]
similar_artists = fetch_similar_artists(mbids)
similar_artist_table.insertmany(
    ('artist_1_id', 'artist_2_id', 'source'),
    ((a['artist_1_id'], a['artist_2_id'], 'echonest')
     for a in similar_artists))
