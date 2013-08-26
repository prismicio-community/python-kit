#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

import prismic

import unittest
import logging
import json
from prismic.exceptions import (InvalidTokenError,
                                AuthorizationNeededError, UnexpectedError)
from test_prismic_fixtures import api_sample_data, search_sample_data

logging.getLogger().setLevel( logging.DEBUG )

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
    def test_search_form(self):
        everything = self.api.form("everything")
        everything.ref("Master")
        docs = everything.submit()
        self.assertTrue(len(docs) == 20)

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


class TestFragmentsTestCase(PrismicTestCase):

    def setUp(self):
        super(TestFragmentsTestCase, self).setUp()
        doc_json = self.search_fixture_data[0]
        self.doc = prismic.Document(doc_json)

    def test_fragments(self):
        print "fragments", self.doc.fragments

    def test_image(self):
        doc = self.doc
        self.assertTrue(doc.get_image("product.image", "main").width == 500)
        self.assertTrue(doc.get_image("product.image", "icon").width == 250)
        expected_html = """<img src="https://wroomio.s3.amazonaws.com/lesbonneschoses/babdc3421037f9af77720d8f5dcf1b84c912c6ba.png" width="250" height="250">"""
        self.assertTrue(expected_html == doc.get_image("product.image", "icon").as_html)

    def test_number(self):
        doc = self.doc
        self.assertTrue(doc.get_number("product.price").__str__() == "3.55")

    def test_color(self):
        doc = self.doc
        self.assertTrue(doc.get_color("product.color").__str__() == "#ffeacd")

    def test_text(self):
        doc = self.doc
        self.assertTrue(doc.get_text("product.allergens").__str__() == "Contains almonds, eggs, milk")

    def test_structured_text_heading(self):
        doc = self.doc
        html = doc.get_html("product.short_lede", lambda x: "/x")
        self.assertTrue(html == "<h2>Crispiness and softness, rolled into one</h2>")

    def test_structured_text_paragraph(self):
        p = prismic.structured_text.StructuredText([span_sample_data])
        p_html = p.as_html(lambda x: "/x")
        print "p_html: ", p_html
        self.assertTrue(p_html == "To <strong><em>be</em></strong> or not <strong>be</strong> ?")

    def test_structured_text_paragraph(self):
        span_sample_data = {"type": "paragraph",
        "text": "To be or not to be ?",
        "spans": [
            {
                "start": 3,
                "end": 5,
                "type": "strong"
            },
            {
                "start": 16,
                "end": 18,
                "type": "strong"
            },
            {
                "start": 3,
                "end": 5,
                "type": "em"
            }
        ]}
        p = prismic.structured_text.StructuredText([span_sample_data])
        p_html = p.as_html(lambda x: "/x")
        print "p_html: ", p_html
        self.assertTrue(p_html == "<p>To <strong><em>be</em></strong> or not to <strong>be</strong> ?</p>")

    # def test_structured_text_paragraph2(self):
    #     span_sample_data = {"type": "paragraph",
    #     "text": "To been or not be ?",
    #     "spans": [
    #         {
    #             "start": 3,
    #             "end": 5,
    #             "type": "strong"
    #         },
    #         {
    #             "start": 16,
    #             "end": 18,
    #             "type": "strong"
    #         },
    #         {
    #             "start": 4,
    #             "end": 6,
    #             "type": "em"
    #         }
    #     ]}
    #     p = prismic.structured_text.StructuredText([span_sample_data])
    #     p_html = p.as_html(lambda x: "/x")
    #     self.assertTrue(p_html == "To <strong>b<em>e</em></strong><em>e</em>n or not <strong>be</strong> ?")

    # def test_st_a(self):
    #     test_paragraph = {
    #         "type": "paragraph",
    #         "text": "bye",
    #         "spans": [
    #             {
    #                 "start": 0,
    #                 "end": 3,
    #                 "type": "hyperlink",
    #                 "data": {
    #                     "type": "Link.document",
    #                     "value": {
    #                         "document": {
    #                             "id": "UbiYbN_mqXkBOgE2",
    #                             "type": "article",
    #                             "tags": [
    #                                 "blog"
    #                             ],
    #                             "slug": "-"
    #                         },
    #                         "isBroken": False
    #                     }
    #                 }
    #             },
    #             {
    #                 "start": 0,
    #                 "end": 3,
    #                 "type": "strong"
    #             }
    #         ]
    #     }
    #     p = prismic.structured_text.StructuredText([test_paragraph])
    #     p_html = p.as_html(lambda x: "/x")
    #     print "p_html: ", p_html
    #     self.assertTrue(p_html == """<a><strong>bye</strong></a>""")
    #     log= logging.getLogger( "SomeTest.testSomething" )



if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFragmentsTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
