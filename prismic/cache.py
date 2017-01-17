# -*- coding: utf-8 -*-

import os
import tempfile
import shelve
from datetime import datetime


class NoCache(object):
    """
    A simple noop implementation for the cache. Any object implementing the same methods
    (duck typing) is acceptable as a cache backend.

    For example, python-memcached is compatible.
    """
    pass

    def set(self, key, val, ttl=0):
        pass

    def get(self, key):
        return None


class ShelveCache(object):
    """
    A cache implementation based on Shelve: https://docs.python.org/2/library/shelve.html.

    By default, it will be created with "filename" equal to the api domain name. If you want to
    run 2 processes using the same repository, you need to set a different file name to avoid
    concurrency problems.
    """
    def __init__(self, filename):
        self.filename = filename
        self.db = None

    def _init_db(self):
        if self.db is None:
            cache_dir = os.path.join(tempfile.mkdtemp(), "prismic-cache")
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            self.db = shelve.open(os.path.join(cache_dir, self.filename))

    def set(self, key, val, ttl=0):
        self._init_db()
        if type(key) != str:
            key = key.encode('utf8')
        self.db[key] = {
            "val": val,
            "expire": ShelveCache.unix_time() + ttl
        }

    def get(self, key):
        self._init_db()
        if type(key) != str:
            key = key.encode('utf8')
        if key not in self.db:
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

