#!/usr/bin/env python
from sqlalchemy.sql import select

from music_graph.apis.echonest import fetch_similar_artists
from music_graph.db.sqla import ENGINE
from music_graph.db.sqla import get_table


artists = get_table('artists')
similar_artists = get_table('similar_artists')
conn = ENGINE.connect()

mbids_q = select([artists.c.id])
mbids = [row[0] for row in conn.execute(mbids_q).fetchall()]
similar_artist_objs = fetch_similar_artists(mbids)
conn.execute(similar_artists.insert(), [
    {
        'artist_1_id': a['artist_1_id'],
        'artist_2_id': a['artist_2_id'],
        'source': 'echonest',
    } for a in similar_artist_objs
])
