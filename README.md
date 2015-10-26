#### Set up a python3 virtualenv for the project
```sh
brew install python3
pip install --upgrade pip virtualenv
virtualenv -p python3 /path/to/virtualenvs/music-graph
. /path/to/virtualenvs/music-graph/bin/activate
pip install -r requirements.txt
```

#### Create library file listing artists in your music library
This will create `data/library.json`
```sh
python library/write_library_file.py /path/to/MyMusicLibrary
```

#### Create initial graph file
This will create `data/graph.json`. The graph has one node per artist and no edges.
```sh
python music_graph/write_initial_graph.py
```

#### Run the server
```sh
python music_graph/app.py
```

Go to http://127.0.0.1:5000/
