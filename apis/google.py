import os

from gmusicapi import Mobileclient

from music_graph.settings import GOOGLE_LIBRARY_FILE
from music_graph.utils import Persistable


USER = os.environ['GOOGLE_USER']
PASSWORD = os.environ['GOOGLE_PASSWORD']


class GoogleLibrary(Persistable):
    file = GOOGLE_LIBRARY_FILE

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
