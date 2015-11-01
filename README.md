![image](https://cloud.githubusercontent.com/assets/52205/10836926/e9ca1d4e-7e70-11e5-9382-78e1fac20f7b.png)

#### Set up a virtualenv
```sh
virtualenv /path/to/virtualenvs/music-graph
. /path/to/virtualenvs/music-graph/bin/activate
pip install -r requirements.txt
python setup.py develop
```

#### Create library file listing artists in your music library
This will create `data/library.json`
```sh
./bin/write_library_file /path/to/MyMusicLibrary
```

#### Fetch Echonest similar artist data
Fetches 100 similar artists per artist. Creates
`data/echonest_similar_artists.json`. First create an echonest account and get
your echonest API key.
```sh
export ECHO_NEST_API_KEY=<ECHONEST_API_KEY>
./bin/write_echonest_similar_artists.py
```

#### Create similar artists playlists in Google Music account
Writes to `data/google_library.json`. You can issue an "app-specific password"
to avoid displaying your main google password in plain text. (But the app-specific
password should still be considered a secret).
```sh
export GOOGLE_USER=<GOOGLE_USERNAME> GOOGLE_PASSWORD=<GOOGLE_PASSWORD>
./bin/fetch_google_library
./bin/add_google_ids_to_library
./bin/create_similar_music_playlists_in_google_account
```

#### Create initial graph file
This will create `data/graph.json`. The graph has one node per artist and no edges.
```sh
./bin/write_initial_graph
```

#### Run the server
```sh
python music_graph/app/server.py
```

Go to http://127.0.0.1:5000/
