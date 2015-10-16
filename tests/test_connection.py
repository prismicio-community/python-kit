#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import prismic
from prismic import connection
import unittest

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        """Teardown."""

    def test_missing_header_key(self):
        headers = {}
        max_age = connection.get_max_age(headers)
        self.assertEqual(max_age, None)

if __name__ == '__main__':
    unittest.main()
