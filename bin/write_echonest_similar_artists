#!/usr/bin/env python
from sqlalchemy.sql import select

from music_graph.apis.echonest import fetch_similar_artists
from music_graph.db.sqla import execute
from music_graph.db.sqla import fetchall
from music_graph.db.sqla import get_table


artists_t = get_table('artists')
similar_artists_t = get_table('similar_artists')

mbids = [row[0] for row in fetchall(select([artists_t.c.id]))]
similar_artist = fetch_similar_artists(mbids)
execute(similar_artists_t.insert(), [
    {
        'artist_1_id': a['artist_1_id'],
        'artist_2_id': a['artist_2_id'],
        'source': 'echonest',
    } for a in similar_artist
])
