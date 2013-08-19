#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

import prismic

import unittest
from prismic.exceptions import (InvalidTokenError,
                                AuthorizationNeededError, HTTPError, UnexpectedError)


class PrismicTestCase(unittest.TestCase):

    def setUp(self):
        """Init the api url and the token identifier."""
        self.api = "http://lesbonneschoses.wroom.io/api"
        self.token = "MC5VZ2phOGRfbXFaOEl2UEpj.dO-_ve-_ve-_ve-_vSFRBzXvv71V77-977-9BO-_vVbvv71k77-9Cu-_ve-_vQTvv71177-9eQpcUE3vv70"

    def tearDown(self):
        """Teardown."""

    def test_get_api(self):
        api = prismic.get(self.api, self.token)
        self.assertTrue(len(api.forms()) > 0)

    def test_authorization_error(self):
        with self.assertRaises(InvalidTokenError):
            prismic.get(self.api, "wrong")

        with self.assertRaises(AuthorizationNeededError):
            prismic.get(self.api, "")

if __name__ == '__main__':
    unittest.main()
