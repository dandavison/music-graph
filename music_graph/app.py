import pickle

import flask
from flask import Flask

from settings import GRAPH_FILE


GRAPH = None
app = Flask(__name__)


@app.route('/', methods=['GET'])
def graph_html():
    return flask.render_template('graph.html', artists=get_artists())


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


def get_artists():
    return GRAPH.nodes()


if __name__ == '__main__':
    with open(GRAPH_FILE, 'rb') as fp:
        GRAPH = pickle.load(fp)
    try:
        app.run(debug=True)
    except:
        with open(GRAPH_FILE, 'wb') as fp:
            pickle.dump(GRAPH, fp)
        raise
