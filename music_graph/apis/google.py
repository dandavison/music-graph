import os

from gmusicapi import Mobileclient

from music_graph.settings import GOOGLE_LIBRARY_FILE
from music_graph.utils import error
from music_graph.utils import Persistable

try:
    USER = os.environ['GOOGLE_USER']
    PASSWORD = os.environ['GOOGLE_PASSWORD']
except KeyError:
    error(
        "Provide your google account login details as environment "
        "variables:\n"
        "export GOOGLE_USER=<username> GOOGLE_PASSWORD=<password>")


class GoogleLibrary(Persistable):
    FILE = GOOGLE_LIBRARY_FILE

    def __init__(self):
        self.data = []

    def to_python(self):
        return self.data

    @classmethod
    def from_python(cls, python):
        instance = cls()
        instance.data = python
        return instance

    def fetch(self):
        client = Mobileclient()
        assert client.login(USER, PASSWORD, Mobileclient.FROM_MAC_ADDRESS)
        self.data = client.get_all_songs()
