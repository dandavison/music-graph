![image](https://cloud.githubusercontent.com/assets/52205/10752496/070dda48-7c47-11e5-953e-7b368ab4f2e4.png)

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
./bin/write_library_file /path/to/MyMusicLibrary
```

#### Create initial graph file
This will create `data/graph.json`. The graph has one node per artist and no edges.
```sh
./bin/write_initial_graph
```

#### Run the server
```sh
python music_graph/server.py
```

Go to http://127.0.0.1:5000/
