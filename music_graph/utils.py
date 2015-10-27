from collections import OrderedDict
import json
import os


class Persistable(object):

    @classmethod
    def load(cls):
        with open(cls.file, 'r') as fp:
            return cls.from_python(
                json.load(fp, object_pairs_hook=OrderedDict))

    def save(self):
        with open(self.file, 'w') as fp:
            fp.write(self.to_json())

    def to_json(self):
        return (json.dumps(self.to_python(), indent=2, sort_keys=True)
                .replace(' \n', '\n'))

    @classmethod
    def from_python(cls, python):
        return cls(**python)


def progress(iterable):
    for i, item in enumerate(iterable):
        yield item
        if not i % 1000:
            print(i)


def file_paths(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            yield os.path.join(dirpath, f)
