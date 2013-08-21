#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

import prismic

import unittest
import json
from prismic.exceptions import (InvalidTokenError,
                                AuthorizationNeededError, UnexpectedError)
from test_prismic_fixtures import api_sample_data, search_sample_data

class PrismicTestCase(unittest.TestCase):
    def setUp(self):
        """Init the api url and the token identifier."""
        self.api_url = "http://lesbonneschoses.wroom.io/api"
        self.token = "MC5VZ2phOGRfbXFaOEl2UEpj.dO-_ve-_ve-_ve-_vSFRBzXvv71V77-977-9BO-_vVbvv71k77-9Cu-_ve-_vQTvv71177-9eQpcUE3vv70"
        self.api_fixture_data = json.loads(api_sample_data)
        self.search_fixture_data = json.loads(search_sample_data)

        self.api = prismic.Api(self.api_fixture_data, self.token)

    def tearDown(self):
        """Teardown."""


class ApiIntegrationTestCase(PrismicTestCase):
    """Doing real HTTP requests to test API data fetching"""

    def test_get_api(self):
        api = prismic.get(self.api_url, self.token)
        self.assertTrue(len(api.forms) > 0)

    def test_api_get_errors(self):
        with self.assertRaises(InvalidTokenError):
            prismic.get(self.api_url, "wrong")

        with self.assertRaises(AuthorizationNeededError):
            prismic.get(self.api_url, "")

        with self.assertRaises(UnexpectedError):
            prismic.get("htt://wrong_on_purpose", "")


class ApiTestCase(PrismicTestCase):
    def test_get_ref(self):
        self.assertTrue(self.api.get_ref("Master").ref == "UgjWQN_mqa8HvPJY")


class TestSearchFormTestCase(PrismicTestCase):
    #def test_search_form(self):
    #    everything = self.api.form("everything")
    #    everything.ref("Master")
    #    docs = everything.submit()
    #    self.assertTrue(len(docs) == 20)

    def test_document(self):
        docs = [prismic.Document(doc) for doc in self.search_fixture_data]
        self.assertTrue(len(docs) == 3)
        doc = docs[0]
        self.assertTrue(doc.slug == "vanilla-macaron")

    def test_empty_slug(self):
        doc_json = self.search_fixture_data[0]
        doc_json["slugs"] = None
        doc = prismic.Document(doc_json)
        self.assertTrue(doc.slug == "-")


if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchFormTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
