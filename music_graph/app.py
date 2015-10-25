import os

from flask import Flask


MUSIC_DIR = os.path.expanduser("~/MusicFuckOffiTunes/")

app = Flask(__name__)


@app.route("/")
def graph():
    artists = os.listdir(MUSIC_DIR)
    return "<br>".join(artists)


if __name__ == "__main__":
    app.run(debug=True)
