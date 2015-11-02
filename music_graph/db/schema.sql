DROP TABLE IF EXISTS artist;
CREATE TABLE artist
(
       id TEXT PRIMARY KEY,
       google_id TEXT,
       echonest_id TEXT,
       name TEXT NOT NULL
);


DROP TABLE IF EXISTS similar_artist;
CREATE TABLE similar_artist
(
       artist_1_id TEXT NOT NULL REFERENCES artist(id) ON DELETE CASCADE,
       artist_2_id TEXT NOT NULL REFERENCES artist(id) ON DELETE CASCADE,
       source TEXT NOT NULL
);
CREATE INDEX similar_artist_1_index ON similar_artist(artist_1_id);
CREATE INDEX similar_artist_2_index ON similar_artist(artist_2_id);


DROP TABLE IF EXISTS track;
CREATE TABLE track
(
        artist_id TEXT NOT NULL REFERENCES artist(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        path TEXT,
        genre TEXT
);
CREATE INDEX track_artist_id_index ON track(artist_id);
