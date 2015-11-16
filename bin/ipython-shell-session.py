from sqlalchemy import select
import sqlalchemy as sqla

from music_graph.db.sqla import fetchall
from music_graph.db.sqla import fetchall_flat
from music_graph.db.sqla import get_table


artists_t = get_table('artists')
google_tracks_t = get_table('google_tracks')
similar_artists_t = get_table('similar_artists')
tracks_t = get_table('tracks')


q = (select([artists_t.c.name])
     .select_from(artists_t.join(similar_artists_t,
                                 similar_artists_t.c.artist_2_id == artists_t.c.id)))
