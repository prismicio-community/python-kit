#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

import prismic

import unittest
import logging
import json
from prismic.exceptions import (InvalidTokenError,
                                AuthorizationNeededError, UnexpectedError)
from test_prismic_fixtures import fixture_api, fixture_search, fixture_structured_lists

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class PrismicTestCase(unittest.TestCase):
    def setUp(self):
        """Init the api url and the token identifier."""
        self.api_url = "http://lesbonneschoses.prismic.io/api"
        self.token = "MC5VZ2phOGRfbXFaOEl2UEpj.dO-_ve-_ve-_ve-_vSFRBzXvv71V77-977-9BO-_vVbvv71k77-9Cu-_ve-_vQTvv71177-9eQpcUE3vv70"
        self.fixture_api = json.loads(fixture_api)
        self.fixture_search = json.loads(fixture_search)
        self.fixture_structured_lists = json.loads(fixture_structured_lists)

        self.api = prismic.Api(self.fixture_api, self.token)

    def tearDown(self):
        """Teardown."""


class ApiIntegrationTestCase(PrismicTestCase):
    """Doing real HTTP requests to test API data fetching"""

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api = prismic.get(self.api_url, self.token)

    def test_get_api(self):
        self.assertTrue(len(self.api.forms) > 0)

    def test_api_get_errors(self):
        with self.assertRaises(InvalidTokenError):
            prismic.get(self.api_url, "wrong")

        with self.assertRaises(AuthorizationNeededError):
            prismic.get(self.api_url, "")

        with self.assertRaises(UnexpectedError):
            prismic.get("htt://wrong_on_purpose", "")

    def test_search_form(self):
        blog = self.api.form("blog")
        blog.ref(self.api.get_master())
        docs = blog.submit()
        self.assertEqual(len(docs), 6)
        self.assertEqual(docs[0].type, "blog-post")


class ApiTestCase(PrismicTestCase):
    def test_get_ref(self):
        self.assertTrue(self.api.get_ref("Master").ref == "UgjWQN_mqa8HvPJY")

    def test_master(self):
        self.assertTrue(self.api.get_master().ref == "UgjWQN_mqa8HvPJY")


class TestSearchFormTestCase(PrismicTestCase):

    def test_document(self):
        docs = [prismic.Document(doc) for doc in self.fixture_search]
        self.assertTrue(len(docs) == 3)
        doc = docs[0]
        self.assertTrue(doc.slug == "vanilla-macaron")

    def test_empty_slug(self):
        doc_json = self.fixture_search[0]
        doc_json["slugs"] = None
        doc = prismic.Document(doc_json)
        self.assertTrue(doc.slug == "-")

    def test_as_html(self):
        doc_json = self.fixture_search[0]
        doc = prismic.Document(doc_json)
        expected_html = """<section data-field="product.allergens"><span class="text">Contains almonds, eggs, milk</span></section><section data-field="product.image"><img src="https://wroomio.s3.amazonaws.com/lesbonneschoses/0417110ebf2dc34a3e8b7b28ee4e06ac82473b70.png" width="500" height="500"></section><section data-field="product.short_lede"><h2>Crispiness and softness, rolled into one</h2></section><section data-field="product.testimonial_author[0]"><h3>Chef Guillaume Bort</h3></section><section data-field="product.related[0]"><a href="document/UdUjvt_mqVNObPeO">dark-chocolate-macaron</a></section><section data-field="product.name"><h1>Vanilla Macaron</h1></section><section data-field="product.related[1]"><a href="document/UdUjsN_mqT1ObPeM">salted-caramel-macaron</a></section><section data-field="product.testimonial_quote[0]"><p>The taste of pure vanilla is very hard to tame, and therefore, most cooks resort to substitutes. <strong>It takes a high-skill chef to know how to get the best of tastes, and <strong><em></strong>Les Bonnes Choses<strong></em></strong>'s vanilla macaron does just that</strong>. The result is more than a success, it simply is a gastronomic piece of art.</p></section><section data-field="product.flavour[0]"><span class="text">Vanilla</span></section><section data-field="product.price"><span class="number">3.55</span></section><section data-field="product.color"><span class="color">#ffeacd</span></section><section data-field="product.description"><p>Experience the ultimate vanilla experience. Our vanilla Macarons are made with our very own (in-house) <strong>pure extract of Madagascar vanilla</strong>, and subtly dusted with <strong>our own vanilla sugar</strong> (which we make from real vanilla beans).</p></section>"""
        doc_html = doc.as_html(lambda link_doc: "document/%s" % link_doc.id)
        self.assertEqual(expected_html, doc_html)

    def test_default_params(self):
        blog = self.api.form("blog")
        self.assertEqual(len(blog.data), 1)
        self.assertEqual(blog.data["q"], ["[[any(document.type, [\"blog-post\"])]]"])

    def test_query_append_value(self):
        blog = self.api.form("blog")
        blog.query("[[bar]]")
        self.assertEqual(len(blog.data), 1)
        self.assertEqual(blog.data["q"], ["[[any(document.type, [\"blog-post\"])]]", "[[bar]]"])

    def test_ref_replace_value(self):
        blog = self.api.form("blog")
        blog.ref("foo")
        self.assertEqual(len(blog.data), 2)
        self.assertEqual(blog.data["ref"], "foo")
        blog.ref("bar")
        self.assertEqual(len(blog.data), 2)
        self.assertEqual(blog.data["ref"], "bar")


class TestFragmentsTestCase(PrismicTestCase):

    def setUp(self):
        super(TestFragmentsTestCase, self).setUp()
        doc_json = self.fixture_search[0]
        self.doc = prismic.Document(doc_json)

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

        text = prismic.Fragment.Text("a&b 42 > 41")
        self.assertEqual(text.as_html, '<span class="text">a&amp;b 42 &gt; 41</span>', "HTML escape")


    def test_structured_text_heading(self):
        doc = self.doc
        html = doc.get_html("product.short_lede", lambda x: "/x")
        self.assertTrue(html == "<h2>Crispiness and softness, rolled into one</h2>")

    def test_structured_text_paragraph(self):
        span_sample_data = {"type": "paragraph",
        "text": "To be or not to be ?",
        "spans": [
            {"start": 3,"end": 5,"type": "strong"},
            { "start": 16, "end": 18, "type": "strong"},
            {"start": 3,"end": 5,"type": "em"}
        ]}
        p = prismic.structured_text.StructuredText([span_sample_data])
        p_html = p.as_html(lambda x: "/x")
        self.assertTrue(p_html == "<p>To <strong><em>be</em></strong> or not to <strong>be</strong> ?</p>")

        p = prismic.structured_text.StructuredText([{"type": "paragraph", "text": "a&b 42 > 41", "spans": []}])
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, "<p>a&amp;b 42 &gt; 41</p>", "Paragraph HTML escape")

        p = prismic.structured_text.StructuredText([{"type": "heading2", "text": "a&b 42 > 41", "spans": []}])
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, "<h2>a&amp;b 42 &gt; 41</h2>", "Header HTML escape")

    def test_lists(self):
        doc_json = self.fixture_structured_lists[0]
        doc = prismic.Document(doc_json)
        doc_html = doc.get_structured_text("article.content").as_html(lambda x: "/x")
        expected = """<h2>A tale of pastry and passion</h2><h2>Here we'll test a list</h2><p>Unordered list:</p><ul><li>Element1</li><li>Element2</li><li>Element3</li></ul><p>Ordered list:</p><ol><li>Element1</li><li>Element2</li><li>Element3</li></ol>"""
        self.assertEqual(doc_html, expected)

    def test_document_link(self):
        test_paragraph = {
            "type": "paragraph",
            "text": "bye",
            "spans": [
                {"start": 0,"end": 3,"type": "hyperlink",
                    "data": {
                        "type": "Link.document",
                        "value": {
                            "document": {"id": "UbiYbN_mqXkBOgE2","type": "article","tags": ["blog"],"slug": "-"},
                            "isBroken": False
                        }
                    }
                },
                {"start": 0,"end": 3,"type": "strong"}
            ]
        }
        p = prismic.structured_text.StructuredText([test_paragraph])

        def link_resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)

        p_html = p.as_html(link_resolver)
        self.assertTrue(p_html == """<p><a href="/document/UbiYbN_mqXkBOgE2/-"><strong>bye</strong></a></p>""")


if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestFragmentsTestCase)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestSearchFormTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
