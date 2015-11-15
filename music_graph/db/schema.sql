DROP TABLE IF EXISTS artists;
CREATE TABLE artists
(
       id TEXT PRIMARY KEY,
       name TEXT NOT NULL,
       google_id TEXT,
       echonest_id TEXT
);


DROP TABLE IF EXISTS similar_artists;
CREATE TABLE similar_artists
(
       artist_1_id TEXT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
       artist_2_id TEXT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
       source TEXT NOT NULL
);
CREATE INDEX similar_artist_1_index ON similar_artists(artist_1_id);
CREATE INDEX similar_artist_2_index ON similar_artists(artist_2_id);


DROP TABLE IF EXISTS tracks;
CREATE TABLE tracks
(
        artist_id TEXT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        path TEXT,
        genre TEXT
);
CREATE INDEX track_artist_id_index ON tracks(artist_id);


DROP TABLE IF EXISTS google_tracks;
CREATE TABLE google_tracks
(
        artist_id TEXT,
        json TEXT NOT NULL
);
