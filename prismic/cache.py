# -*- coding: utf-8 -*-

import os
import shelve
from datetime import datetime


class NoCache(object):
    """
    A simple noop implementation for the cache. Any object implementing the same methods
    (duck typing) is acceptable as a cache backend.

    For example, python-memcached is compatible.
    """
    pass

    def set(self, key, val, time=0):
        pass

    def get(self, key):
        return None


class ShelveCache(object):
    """
    A cache implementation based on Shelve: https://docs.python.org/2/library/shelve.html.
    """
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.db = shelve.open(os.path.join(script_dir, "cache"))

    def set(self, key, val, time=0):
        self.db[key] = {
            "val": val,
            "expire": ShelveCache.unix_time() + time
        }

    def get(self, key):
        if not key in self.db:
            return None
        d = self.db[key]
        if d["expire"] < ShelveCache.unix_time():
            del self.db[key]
            return None
        else:
            return d["val"]

    @staticmethod
    def unix_time():
        epoch = datetime.utcfromtimestamp(0)
        delta = datetime.now() - epoch
        return delta.total_seconds()

