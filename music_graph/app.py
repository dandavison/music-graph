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
    # Required by d3.js?
    graph = GRAPH.copy()
    for n in graph:
        graph.node[n]['name'] = n

    return flask.jsonify(graph.to_python())


@app.route('/graph/edges', methods=['POST'])
def create_edge():
    form = flask.request.form
    artist_1, artist_2 = form['Artist_1'], form['Artist_2']

    def is_valid(name):
        return name in GRAPH.get_artist_names()

    if is_valid(artist_1) and is_valid(artist_2):
        GRAPH.add_edge(artist_1, artist_2)
        GRAPH.save()

    return flask.redirect('/')


if __name__ == '__main__':
    GRAPH = MusicGraph.load()
    app.run(debug=True)
