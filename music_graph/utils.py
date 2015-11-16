from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
import json
import os
import sys
import time

from fish import ProgressFish

THIRTY_SECONDS = timedelta(seconds=30)


class Persistable(object):

    @classmethod
    def load(cls):
        with open(cls.FILE, 'r') as fp:
            return cls.from_python(
                json.load(fp, object_pairs_hook=OrderedDict))

    def save(self):
        with open(self.FILE, 'w') as fp:
            fp.write(self.to_json())

    def to_json(self):
        return (json.dumps(self.to_python(), indent=2, sort_keys=True)
                .replace(' \n', '\n'))

    @classmethod
    def from_python(cls, python):
        return cls(**python)


def info(msg):
    print msg


def error(msg):
    print >>sys.stderr, msg


def debug(msg):
    if False:
        print >>sys.stderr, msg


def warn(msg):
    print >>sys.stderr, msg


def by(key, dicts):
    return {d[key]: d for d in dicts}


def round_robin(iterators):
    """
    Yield items from iterators until exhaustion.

    Yield an item from each non-exhausted iterator in turn, until all are
    exhausted.
    """
    n_iterables = len(iterators)
    while iterators:
        for iterator in list(iterators):
            try:
                yield next(iterator)
            except StopIteration:
                iterators.remove(iterator)


def progress(iterable, total):
    fish = ProgressFish(total=total)
    for i, item in enumerate(iterable):
        yield item
        fish.animate(amount=i)


def rate_limit(iterable, interval):
    interval = timedelta(seconds=interval)
    last_time = datetime.now() - interval
    for item in iterable:
        waited = datetime.now() - last_time
        if waited < interval:
            time.sleep((interval - waited).total_seconds())
        last_time = datetime.now()
        yield item


def repeat_until_success(fn, interval):
    while True:
        try:
            return fn()
        except:
            if interval:
                warn("Pausing for %ds" % interval)
                time.sleep(interval)


def wait_until(fn, timeout=THIRTY_SECONDS, sleep=1):
    start = datetime.now()
    while True:
        if fn():
            return
        elif datetime.now() - start > timeout:
            raise RuntimeError("Timeout")
        else:
            time.sleep(sleep)


def file_paths(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            yield os.path.join(dirpath, f).decode('utf-8')
