import os

import flask
from flask import Flask

from sqlalchemy.sql import select

from music_graph.db.sqla import fetchall_flat
from music_graph.db.sqla import get_table
from music_graph.graph import MusicGraph


GRAPH = None
app = Flask(__name__)


class ValidationError(Exception):
    pass


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
    tracks_t = get_table('tracks')
    path = fetchall_flat(select([tracks_t.c.path])
                         .where(tracks_t.c.artist_id == artist_id))[0]
    os.system('open "%s"' % path)
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
    GRAPH = MusicGraph.load()
    print("Loaded graph with %d nodes and %d edges" % (
        GRAPH.number_of_nodes(),
        GRAPH.number_of_edges()))
    app.run(debug=True)
