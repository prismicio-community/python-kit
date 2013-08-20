#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

import prismic

import unittest
import json
from prismic.exceptions import (InvalidTokenError,
                                AuthorizationNeededError, UnexpectedError)

api_sample_data = """
{
    "refs": [{
        "ref": "UgjWQN_mqa8HvPJY",
        "label": "Master",
        "isMasterRef": true
    }, {
        "ref": "UgjWRd_mqbYHvPJa",
        "label": "San Francisco Grand opening"
    }],
    "bookmarks": {
        "about": "Ue0EDd_mqb8Dhk3j",
        "jobs": "Ue0EHN_mqbwDhk3l",
        "stores": "Ue0EVt_mqd8Dhk3n"
    },
    "types": {
        "blog-post": "Blog post",
        "store": "Store",
        "article": "Site-level article",
        "selection": "Products selection",
        "job-offer": "Job offer",
        "product": "Product"
    },
    "tags": ["Cupcake", "Pie", "Featured", "Macaron"],
    "forms": {
        "everything": {
            "method": "GET",
            "enctype": "application/x-www-form-urlencoded",
            "action": "http://lesbonneschoses.wroom.io/api/documents/search",
            "fields": {
                "ref": {
                    "type": "String"
                },
                "q": {
                    "type": "String"
                }
            }
        }
    },
    "oauth_initiate": "http://lesbonneschoses.wroom.io/auth",
    "oauth_token": "http://lesbonneschoses.wroom.io/auth/token"
}"""

class PrismicTestCase(unittest.TestCase):
    def setUp(self):
        """Init the api url and the token identifier."""
        self.api = "http://lesbonneschoses.wroom.io/api"
        self.token = "MC5VZ2phOGRfbXFaOEl2UEpj.dO-_ve-_ve-_ve-_vSFRBzXvv71V77-977-9BO-_vVbvv71k77-9Cu-_ve-_vQTvv71177-9eQpcUE3vv70"
        self.api_sample_data = json.loads(api_sample_data)
        self.refLabel = "Master"

    def tearDown(self):
        """Teardown."""


class ApiTestCase(PrismicTestCase):

    def test_get_api(self):
        api = prismic.get(self.api, self.token)
        self.assertTrue(len(api.forms) > 0)

    def test_api_get_errors(self):
        with self.assertRaises(InvalidTokenError):
            prismic.get(self.api, "wrong")

        with self.assertRaises(AuthorizationNeededError):
            prismic.get(self.api, "")

        with self.assertRaises(UnexpectedError):
            prismic.get("htt://wrong_on_purpose", "")


class TestSearchFormTestCase(PrismicTestCase):
    def test_search_form(self):
        api = prismic.Api(self.api_sample_data, self.token)
        everything = api.get_form("everything")
        everything.ref_by_label("Master")
        result = everything.submit()
        print(result)


if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchFormTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
