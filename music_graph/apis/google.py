import os

from gmusicapi import Mobileclient

from music_graph.utils import error


try:
    USER = os.environ['GOOGLE_USER']
    PASSWORD = os.environ['GOOGLE_PASSWORD']
except KeyError:
    error(
        "Provide your google account login details as environment "
        "variables:\n"
        "export GOOGLE_USER=<username> GOOGLE_PASSWORD=<password>")


def fetch_all_tracks():
    client = Mobileclient()
    assert client.login(USER, PASSWORD, Mobileclient.FROM_MAC_ADDRESS)
    return client.get_all_songs()
