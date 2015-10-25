import os

from flask import jsonify
from flask import Flask
from flask import render_template

import networkx as nx
from networkx.readwrite import json_graph


MUSIC_DIR = os.path.expanduser("~/MusicFuckOffiTunes/")

app = Flask(__name__)


@app.route("/")
def graph_html():
    return render_template('graph.html')


@app.route("/graph")
def graph_json():
    g = make_graph()
    return jsonify(json_graph.node_link_data(g))


def make_graph():
    artists = os.listdir(MUSIC_DIR)

    group_fn = lambda artist: int(a[0].lower() < 'm')

    groups = {
        0: [],
        1: [],
    }
    for a in artists:
        groups[group_fn(a)].append(a)

    g = nx.Graph()
    for a1, a2 in zip(groups[0], groups[1]):
        g.add_edge(a1, a2)

    for n in g:
        g.node[n]['name'] = n

    return g


if __name__ == "__main__":
    app.run(debug=True)
