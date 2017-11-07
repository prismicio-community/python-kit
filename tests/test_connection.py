#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import prismic
from prismic import connection
import unittest


class ConnectionTestCase(unittest.TestCase):

    def test_missing_header_key(self):
        headers = {}
        max_age = connection.get_max_age(headers)
        self.assertEqual(max_age, None)

    def test_long_key(self):
        """
        Test we can cache long keys

        Some cache backends can't handle keys longer than 250 characters (like memcached)
        """

        def fake_request_handler(url):
            return 200, '{}', {}

        class ShortKeyCache(object):

            def set(self, key, value, expires):
                if len(key) > 250:
                    raise Exception('key too long')

            def get(self, key):
                pass

        long_key = 'http://unittest.prismic.io/' + ('a' * 300)
        connection.get_json(long_key, request_handler=fake_request_handler, cache=ShortKeyCache(), ttl=5)

if __name__ == '__main__':
    unittest.main()
