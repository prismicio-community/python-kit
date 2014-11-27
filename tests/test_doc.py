#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

from prismic.cache import ShelveCache, NoCache
from prismic.exceptions import InvalidTokenError, AuthorizationNeededError, \
    UnexpectedError
from .test_prismic_fixtures import fixture_api, fixture_search, fixture_groups, \
    fixture_structured_lists, fixture_empty_paragraph, fixture_store_geopoint, \
    fixture_image_links, fixture_spans_labels, fixture_block_labels, fixture_custom_html
import json
import logging
import datetime
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
        api = prismic.get("https://lesbonneschoses.cdn.prismic.io/api")
        # endgist
        self.assertIsNotNone(api)

    def test_simplequery(self):
        # startgist:848271920fc502fb82d1:prismic-simplequery.py
        api = prismic.get("https://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master())\
            .query(predicates.at("document.type", "product"))\
            .submit()
        # endgist
        self.assertEqual(response.results_size, 16)

    def test_api_private(self):
        try:
            # startgist:71fbe142e1078f0ff76b:prismic-apiPrivate.py
            # This will fail because the token is invalid, but this is how to access a private API
            api = prismic.get('https://lesbonneschoses.prismic.io/api', 'MC5-XXXXXXX-vRfvv70')
            # endgist
            self.fail('Should have thrown')  # gisthide
        except InvalidTokenError as e:
            pass

    def test_references(self):
        # startgist:8061f7a1028d4f55dd63:prismic-references.py
        preview_token = 'MC5VbDdXQmtuTTB6Z0hNWHF3.c--_vVbvv73vv73vv73vv71EA--_vS_vv73vv70T77-9Ke-_ve-_vWfvv70ebO-_ve-_ve-_vQN377-9ce-_vRfvv70'
        api = prismic.get('https://lesbonneschoses.prismic.io/api', preview_token)
        st_patrick_ref = api.get_ref('St-Patrick specials')
        # Now we'll use this reference for all our calls
        response = api.form("everything")\
            .ref(st_patrick_ref)\
            .query(predicates.at("document.type", "product"))\
            .submit()
        # The documents object contains a Response object with all documents of type "product"
        # including the new "Saint-Patrick's Cupcake"
        # endgist
        self.assertEqual(response.results_size, 17)

    def test_orderings(self):
        # startgist:88098ee61f2f982ae9d6:prismic-orderings.py
        api = prismic.get('https://lesbonneschoses.prismic.io/api')
        response = api.form('everything')\
            .ref(api.get_master())\
            .query(predicates.at("document.type", "product"))\
            .pageSize(100)\
            .orderings('[my.product.price desc]')\
            .submit()
        # The products are now ordered by price, highest first
        results = response.results
        # endgist
        self.assertEqual(response.results_per_page, 100)

    def test_predicates(self):
        # startgist:75f170c0950a97b57896:prismic-predicates.py
        api = prismic.get("http://lesbonneschoses.prismic.io/api")
        response = api.form("everything").ref(api.get_master()) \
            .query(predicates.at("document.type", "product"),
                   predicates.date_after("my.blog-post.date", 1401580800000))\
            .submit()
        # endgist
        self.assertEqual(response.results_size, 0)

    def test_all_predicates(self):
        # startgist:057350d746fa64a673df:prismic-allPredicates.py
        # "at" predicate: equality of a fragment to a value.
        at = predicates.at("document.type", "article")
        # "any" predicate: equality of a fragment to a value.
        any = predicates.any("document.type", ["article", "blog-post"])
        # "fulltext" predicate: fulltext search in a fragment.
        fulltext = predicates.fulltext("my.article.body", "sausage")
        # "similar" predicate, with a document id as reference
        similar = predicates.similar("UXasdFwe42D", 10)
        # endgist
        self.assertEqual(at, ["at", "document.type", "article"])
        self.assertEqual(any, ["any", "document.type", ["article", "blog-post"]])

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

    def test_get_text(self):
        api = prismic.get('https://lesbonneschoses.prismic.io/api')
        response = api.form('everything').query(predicates.at("document.id", "UlfoxUnM0wkXYXbl"))\
            .ref(api.get_master()).submit()
        doc = response.documents[0]
        # // startgist:d06042ce84f6002c055d:prismic-getText.py
        author = doc.get_text("blog-post.author")
        if author is None:
            author = "Anonymous"
        # endgist
        self.assertEqual(author, "John M. Martelle, Fine Pastry Magazine")

    def test_get_number(self):
        api = prismic.get('https://lesbonneschoses.prismic.io/api')
        response = api.form('everything').query(predicates.at("document.id", "UlfoxUnM0wkXYXbO"))\
            .ref(api.get_master()).submit()
        doc = response.documents[0]
        # startgist:2542ea501c2f950c597e:prismic-getNumber.py
        # Number predicates
        gt = predicates.gt("my.product.price", 10)
        lt = predicates.lt("my.product.price", 20)
        in_range = predicates.in_range("my.product.price", 10, 20)

        # Accessing number fields
        price = doc.get_number("product.price").value
        # endgist
        self.assertEqual(price, 2.5)

    def test_images(self):
        api = prismic.get('https://lesbonneschoses.prismic.io/api')
        response = api.form('everything').query(predicates.at("document.id", "UlfoxUnM0wkXYXbO")) \
            .ref(api.get_master()).submit()
        doc = response.documents[0]
        # startgist:360d054f79680bd48679:prismic-images.py
        # Accessing image fields
        image = doc.get_image('product.image')
        # By default the 'main' view is returned
        url = image.url
        # endgist
        self.assertEqual(
            url,
            'https://prismic-io.s3.amazonaws.com/lesbonneschoses/f606ad513fcc2a73b909817119b84d6fd0d61a6d.png')

    def test_date_timestamp(self):
        api = prismic.get('https://lesbonneschoses.prismic.io/api')
        response = api.form('everything').query(predicates.at("document.id", "UlfoxUnM0wkXYXbl"))\
            .ref(api.get_master()).submit()
        doc = response.documents[0]
        # startgist:a416bcf69d3e604d5c3b:prismic-dateTimestamp.py
        # Date and Timestamp predicates
        date_before = predicates.date_before("my.product.releaseDate", datetime.datetime(2014, 6, 1))
        date_after = predicates.date_after("my.product.releaseDate", datetime.datetime(2014, 1, 1))
        date_Between = predicates.date_between("my.product.releaseDate", datetime.datetime(2014, 1, 1), datetime.datetime(2014, 6, 1))
        day_of_month = predicates.day_of_month("my.product.releaseDate", 14)
        day_of_month_after = predicates.day_of_month_after("my.product.releaseDate", 14)
        day_of_month_before = predicates.day_of_month_before("my.product.releaseDate", 14)
        day_of_week = predicates.day_of_week("my.product.releaseDate", "Tuesday")
        day_of_week_after = predicates.day_of_week_after("my.product.releaseDate", "Wednesday")
        day_of_week_before = predicates.day_of_month_before("my.product.releaseDate", "Wednesday")
        month = predicates.month("my.product.releaseDate", "June")
        month_before = predicates.month_before("my.product.releaseDate", "June")
        month_after = predicates.month_after("my.product.releaseDate", "June")
        year = predicates.year("my.product.releaseDate", 2014)
        hour = predicates.hour("my.product.releaseDate", 12)
        hour_before = predicates.hour_before("my.product.releaseDate", 12)
        hour_after = predicates.hour_after("my.product.releaseDate", 12)

        # Accessing Date and Timestamp fields
        date = doc.get_date("blog-post.date")
        date_year = date and date.as_datetime.year
        update_time = doc.get_timestamp("blog-post.update")
        update_hour = update_time and update_time.as_datetime.hours
        # endgist
        self.assertEqual(date_year, 2013)

    def test_group(self):
        data = "{\"id\":\"abcd\",\"type\":\"article\",\"href\":\"\",\"slugs\":[],\"tags\":[],\"data\":{\"article\":{\"documents\":{\"type\":\"Group\",\"value\":[{\"linktodoc\":{\"type\":\"Link.document\",\"value\":{\"document\":{\"id\":\"UrDejAEAAFwMyrW9\",\"type\":\"doc\",\"tags\":[],\"slug\":\"installing-meta-micro\"},\"isBroken\":false}},\"desc\":{\"type\":\"StructuredText\",\"value\":[{\"type\":\"paragraph\",\"text\":\"A detailed step by step point of view on how installing happens.\",\"spans\":[]}]}},{\"linktodoc\":{\"type\":\"Link.document\",\"value\":{\"document\":{\"id\":\"UrDmKgEAALwMyrXA\",\"type\":\"doc\",\"tags\":[],\"slug\":\"using-meta-micro\"},\"isBroken\":false}}}]}}}}"
        document = prismic.Document(json.loads(data))
        def resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)
        # startgist:8618c84784a22634ca6a:prismic-group.py
        group = document.get_group("article.documents")
        docs = (group and group.value) or []
        for doc in docs:
            desc = doc.get_structured_text("desc")
            link = doc.get_link("linktodoc")
        # endgist
        self.assertEqual(docs[0].get_structured_text("desc").as_html(resolver), "<p>A detailed step by step point of view on how installing happens.</p>")

    def test_link(self):
        data = "{\"id\":\"abcd\",\"type\":\"article\",\"href\":\"\",\"slugs\":[],\"tags\":[],\"data\":{\"article\":{\"source\":{\"type\":\"Link.document\",\"value\":{\"document\":{\"id\":\"UlfoxUnM0wkXYXbE\",\"type\":\"product\",\"tags\":[\"Macaron\"],\"slug\":\"dark-chocolate-macaron\"},\"isBroken\":false}}}}}"
        document = prismic.Document(json.loads(data))
        # startgist:1417c3a9baf3015e34b8:prismic-link.py
        def resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)
        source = document.get_link("article.source")
        url = source and source.get_url(resolver)
        # endgist
        self.assertEqual(url, "/document/UlfoxUnM0wkXYXbE/dark-chocolate-macaron")

    def test_embed(self):
        data = "{\"id\":\"abcd\",\"type\":\"article\",\"href\":\"\",\"slugs\":[],\"tags\":[],\"data\":{\"article\":{\"video\":{\"type\":\"Embed\",\"value\":{\"oembed\":{\"provider_url\":\"http://www.youtube.com/\",\"type\":\"video\",\"thumbnail_height\":360,\"height\":270,\"thumbnail_url\":\"http://i1.ytimg.com/vi/baGfM6dBzs8/hqdefault.jpg\",\"width\":480,\"provider_name\":\"YouTube\",\"html\":\"<iframe width=\\\"480\\\" height=\\\"270\\\" src=\\\"http://www.youtube.com/embed/baGfM6dBzs8?feature=oembed\\\" frameborder=\\\"0\\\" allowfullscreen></iframe>\",\"author_name\":\"Siobhan Wilson\",\"version\":\"1.0\",\"author_url\":\"http://www.youtube.com/user/siobhanwilsonsongs\",\"thumbnail_width\":480,\"title\":\"Siobhan Wilson - All Dressed Up\",\"embed_url\":\"https://www.youtube.com/watch?v=baGfM6dBzs8\"}}}}}}"
        document = prismic.Document(json.loads(data))
        # startgist:f405d95bc1d987aedeaa:prismic-embed.py
        video = document.get_embed("article.video")
        # Html is the code to include to embed the object, and depends on the embedded service
        html = video and video.as_html
        # endgist
        self.assertEqual(html, "<div data-oembed=\"https://www.youtube.com/watch?v=baGfM6dBzs8\" data-oembed-type=\"video\" data-oembed-provider=\"YouTube\"><iframe width=\"480\" height=\"270\" src=\"http://www.youtube.com/embed/baGfM6dBzs8?feature=oembed\" frameborder=\"0\" allowfullscreen></iframe></div>")

    def test_color(self):
        data = "{\"id\":\"abcd\",\"type\":\"article\",\"href\":\"\",\"slugs\":[],\"tags\":[],\"data\":{\"article\":{\"background\":{\"type\":\"Color\",\"value\":\"#000000\"}}}}"
        document = prismic.Document(json.loads(data))
        # startgist:85a630064368ebabf2e6:prismic-color.py
        bgcolor = document.get_color("article.background")
        hex = bgcolor.value
        # endgist
        self.assertEqual(hex, "#000000")

    def test_geopoint(self):
        data = "{\"id\":\"abcd\",\"type\":\"article\",\"href\":\"\",\"slugs\":[],\"tags\":[],\"data\":{\"article\":{\"location\":{\"type\":\"GeoPoint\",\"value\":{\"latitude\":48.877108,\"longitude\":2.333879}}}}}"
        document = prismic.Document(json.loads(data))
        # startgist:316cb72c1a5789fd2049:prismic-geopoint.py
        # "near" predicate for GeoPoint fragments
        near = predicates.near("my.store.location", 48.8768767, 2.3338802, 10)

        # Accessing GeoPoint fragments
        place = document.get_geopoint("article.location")
        coordinates = place and ("%.6f,%.6f" % (place.latitude, place.longitude))
        # endgist
        self.assertEqual(coordinates, "48.877108,2.333879")

    def test_cache(self):
        # startgist:11a75574ad42c60ff6de:prismic-cache.py
        # Just implement your own cache object by duck-typing
        # https://github.com/prismicio/python-kit/blob/master/prismic/cache.py
        no_cache = NoCache()
        # This api will use the custom cache object
        api = prismic.get('https://lesbonneschoses.prismic.io/api', cache=no_cache)
        # endgist
        self.assertIsNotNone(api)


if __name__ == '__main__':
    unittest.main()

