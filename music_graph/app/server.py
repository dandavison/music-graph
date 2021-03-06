import json
import os

import flask
from flask import Flask

from music_graph.graph import MusicGraph
from music_graph.library import MusicLibrary


LIBRARY = None
GRAPH = None
app = Flask(__name__)


@app.route('/', methods=['GET'])
def graph_html():
    return flask.render_template('graph.html',
                                 artists=sorted(GRAPH.get_artist_names()))


@app.route('/graph', methods=['GET'])
def graph_json():
    return flask.jsonify(GRAPH.to_python())


@app.route('/graph/edges', methods=['POST'])
def create_edge():
    form = flask.request.form
    artist_1, artist_2 = form['Artist_1'], form['Artist_2']

    if _is_valid_edge(artist_1, artist_2):
        GRAPH.add_edge(artist_1, artist_2)
    GRAPH.save()

    return flask.redirect('/')


@app.route('/play', methods=['POST'])
def play_artist():
    artist_id = flask.request.args['artist_id']
    track = LIBRARY.data[artist_id]['tracks'][0]
    os.system('open "%s"' % track['path'])
    return flask.redirect('/')


def validate_artist(artist):
    if artist not in GRAPH.get_artist_names():
        raise ValidationError
    return artist


def _is_valid_edge(artist_1, artist_2):
    return (validate_artist(artist_1) and
            validate_artist(artist_2) and
            artist_1 != artist_2)


if __name__ == '__main__':
    LIBRARY = MusicLibrary.load()
    print("Loaded library of %d artists" % len(LIBRARY.data))
    GRAPH = MusicGraph.load()
    print("Loaded graph with %d nodes and %d edges" % (GRAPH.number_of_nodes(),
                                                       GRAPH.number_of_edges()))
    app.run(debug=True)
