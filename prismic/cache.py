# -*- coding: utf-8 -*-


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
