#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

from prismic.cache import ShelveCache
from prismic.exceptions import InvalidTokenError, AuthorizationNeededError, \
    UnexpectedError
from .test_prismic_fixtures import fixture_api, fixture_search, fixture_groups, \
    fixture_structured_lists, fixture_empty_paragraph, fixture_store_geopoint, \
    fixture_image_links, fixture_spans_labels, fixture_block_labels, fixture_custom_html
import json
import logging
import prismic
from prismic import predicates
import unittest

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class DocTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        """Teardown."""

    def test_api(self):
        # startgist:13972e11d41ca29c0171:prismic-api.py
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        # endgist
        self.assertIsNotNone(api)

    def test_simplequery(self):
        # startgist:848271920fc502fb82d1:prismic-simplequery.py
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master())\
            .query(predicates.at("document.type", "product"))\
            .submit()
        # endgist
        self.assertEqual(response.results_size, 16)

    def test_predicates(self):
        # startgist:75f170c0950a97b57896:prismic-predicates.py
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master()) \
            .query(predicates.at("document.type", "product"),
                   predicates.date_after("my.blog-post.date", 1401580800000))\
            .submit()
        # endgist
        self.assertEqual(response.results_size, 0)

    def test_as_html(self):
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master())\
            .query(predicates.at("document.id", "UlfoxUnM0wkXYXbX")).submit()
        # startgist:12326c99257882585e0d:prismic-asHtml.py
        def link_resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)
        doc = response.documents[0]
        html = doc.as_html(link_resolver)
        # endgist
        self.assertIsNotNone(html)

    def test_html_serializer(self):
        # startgist:dcf171c8e047f43e0472:prismic-htmlSerializer.py
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master()) \
            .query(predicates.at("document.id", "UlfoxUnM0wkXYXbX")).submit()

        def link_resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)

        def html_serializer(element, content):
            if isinstance(element, prismic.fragments.Block.Image):
                # Don't wrap images in a <p> tag
                return element.get_view().as_html(link_resolver)
            if isinstance(element, prismic.fragments.Span.Hyperlink):
                # Add a class to links
                return """<a class="some-link" href="%s">""" % element.get_url(link_resolver) + content + "</a>"
            return None

        doc = response.documents[0]
        html = doc.get_structured_text("blog-post.body").as_html(link_resolver, html_serializer)
        # endgist
        self.assertIsNotNone(html)


if __name__ == '__main__':
    unittest.main()

