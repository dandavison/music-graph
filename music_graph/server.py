import json

import flask
from flask import Flask

from graph import MusicGraph


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


def _is_valid_edge(artist_1, artist_2):
    def is_valid(name):
        return name in GRAPH.get_artist_names()

    return (is_valid(artist_1) and
            is_valid(artist_2) and
            artist_1 != artist_2)


if __name__ == '__main__':
    GRAPH = MusicGraph.load()
    print("Loaded graph with %d nodes and %d edges" % (GRAPH.number_of_nodes(),
                                                       GRAPH.number_of_edges()))
    app.run(debug=True)
