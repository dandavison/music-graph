import json

import flask
from flask import Flask

from graph import MusicGraph


GRAPH = None
app = Flask(__name__)


@app.route('/', methods=['GET'])
def graph_html():
    return flask.render_template('graph.html', artists=GRAPH.nodes())


@app.route('/graph', methods=['GET'])
def graph_json():
    # FIXME: do on copy
    for n in GRAPH:
        GRAPH.node[n]['name'] = n

    return flask.jsonify(GRAPH.to_python())


@app.route('/graph/edges', methods=['POST'])
def create_edge():
    form = flask.request.form
    GRAPH.add_edge(form['Artist_1'], form['Artist_2'])
    return flask.redirect('/')


if __name__ == '__main__':
    GRAPH = MusicGraph.load()
    app.run(debug=True)
