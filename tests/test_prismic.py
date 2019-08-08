#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Prismic library"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

from prismic.cache import ShelveCache
from prismic.exceptions import InvalidTokenError, AuthorizationNeededError, InvalidURLError
from .test_prismic_fixtures import fixture_api, fixture_search, fixture_groups, \
    fixture_structured_lists, fixture_empty_paragraph, fixture_store_geopoint, fixture_image_links, \
    fixture_spans_labels, fixture_block_labels, fixture_custom_html, fixture_slices, fixture_composite_slices
import time
import json
import logging
import prismic
from prismic import predicates
import unittest

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)


class PrismicTestCase(unittest.TestCase):
    def setUp(self):
        """Init the api url and the token identifier."""
        self.api_url = "http://micro.prismic.io/api"
        self.token = "MC5VcXBHWHdFQUFONDZrbWp4.77-9cDx6C3lgJu-_vXZafO-_vXPvv73vv73vv70777-9Ju-_ve-_vSLvv73vv73vv73vv70O77-977-9Me-_vQ"
        self.fixture_api = json.loads(fixture_api)
        self.fixture_search = json.loads(fixture_search)
        self.fixture_structured_lists = json.loads(fixture_structured_lists)
        self.fixture_empty_paragraph = json.loads(fixture_empty_paragraph)
        self.fixture_block_labels = json.loads(fixture_block_labels)
        self.fixture_store_geopoint = json.loads(fixture_store_geopoint)
        self.fixture_groups = json.loads(fixture_groups)
        self.fixture_image_links = json.loads(fixture_image_links)
        self.fixture_spans_labels = json.loads(fixture_spans_labels)
        self.fixture_custom_html = json.loads(fixture_custom_html)
        self.fixture_slices = json.loads(fixture_slices)
        self.fixture_composite_slices = json.loads(fixture_composite_slices)

        self.api = prismic.Api(self.fixture_api, self.token, ShelveCache("prismictest"), None)

    def tearDown(self):
        """Teardown."""

    @staticmethod
    def link_resolver(document_link):
        if document_link.is_broken:
            return "#broken"
        else:
            return "/document/%s/%s" % (document_link.id, document_link.slug)

    @staticmethod
    def html_serializer(element, content):
        if isinstance(element, prismic.fragments.Block.Image):
            return element.get_view().as_html(PrismicTestCase.link_resolver)
        if isinstance(element, prismic.fragments.Span.Hyperlink):
            return """<a class="some-link" href="%s">""" % element.get_url(PrismicTestCase.link_resolver) + content + "</a>"
        return None


class ApiIntegrationTestCase(PrismicTestCase):
    """Doing real HTTP requests to test API data fetching"""

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api = prismic.get(self.api_url, self.token)

    def test_get_api(self):
        self.assertGreater(len(self.api.forms), 0)

    def test_api_get_errors(self):
        with self.assertRaises(InvalidTokenError):
            prismic.get(self.api_url, "wrong")

        with self.assertRaises(AuthorizationNeededError):
            prismic.get(self.api_url, "")

        with self.assertRaises(InvalidURLError):
            prismic.get("htt://wrong_on_purpose", "")

    def test_search_form(self):
        form = self.api.form("everything")
        form.ref(self.api.get_master())
        docs = form.submit().documents
        self.assertGreaterEqual(len(docs), 2)

    def test_search_form_orderings(self):
        form = self.api.form("everything")
        form.ref(self.api.get_master())
        form.query('[[:q = at(document.type, "all")]]')
        form.orderings("[my.all.number]")
        docs = form.submit().documents
        self.assertEqual(docs[0].uid, 'all')
        self.assertEqual(docs[1].uid, 'all1')
        self.assertEqual(docs[2].uid, 'all2')

    def test_search_form_page_size(self):
        form = self.api.form("everything").page_size(2)
        form.ref(self.api.get_master())
        response = form.submit()
        self.assertEqual(len(response.documents), 2)
        self.assertEqual(response.results_per_page, 2)

    def test_search_form_first_page(self):
        form = self.api.form("everything").pageSize(2)
        form.ref(self.api.get_master())
        response = form.submit()
        self.assertEqual(response.page, 1)
        self.assertEqual(len(response.documents), 2)
        self.assertEqual(response.results_size, len(response.documents))
        self.assertIsNone(response.prev_page)
        self.assertIsNotNone(response.next_page)

    def test_search_form_page(self):
        form = self.api.form("everything").pageSize(2).page(2)
        form.ref(self.api.get_master())
        response = form.submit()
        self.assertEqual(response.page, 2)
        self.assertEqual(len(response.documents), 2)
        self.assertEqual(response.results_size, len(response.documents))
        self.assertIsNotNone(response.prev_page)
        self.assertIsNotNone(response.next_page)

    def test_search_form_count(self):
        form = self.api.form("everything")
        form.ref(self.api.get_master())
        nb_docs = form.count()
        self.assertGreaterEqual(nb_docs, 2)

    def test_query(self):
        doc = self.api\
            .query(predicates.at('document.id', 'WHx-gSYAAMkyXYX_'))\
            .documents[0]
        self.assertEqual(doc.id, 'WHx-gSYAAMkyXYX_')

    def test_query_first(self):
        doc = self.api.query_first(predicates.at('document.id', 'WHx-gSYAAMkyXYX_'))
        self.assertEqual(doc.id, 'WHx-gSYAAMkyXYX_')

    def test_query_first_no_result(self):
        doc = self.api.query_first(predicates.at('document.id', 'NotAValidId'))
        self.assertIsNone(doc)

    def test_get_by_uid(self):
        doc = self.api.get_by_uid('all', 'all')
        self.assertEqual(doc.id, 'WHx-gSYAAMkyXYX_')

    def test_get_by_id(self):
        doc = self.api.get_by_id('WHx-gSYAAMkyXYX_')
        self.assertEqual(doc.id, 'WHx-gSYAAMkyXYX_')

    def test_get_by_ids(self):
        result = self.api.get_by_ids(['WHx-gSYAAMkyXYX_', 'WHyJqyYAAHgyXbcj'])
        ids = sorted([doc.id for doc in result.documents])
        self.assertEqual(ids[0], 'WHx-gSYAAMkyXYX_')
        self.assertEqual(ids[1], 'WHyJqyYAAHgyXbcj')

    def test_get_single(self):
        doc = self.api.get_single('single')
        self.assertEqual(doc.id, 'V_OplCUAACQAE0lA')

    def test_linked_documents(self):
        doc = self.api\
            .form("everything")\
            .ref(self.api.get_master())\
            .query('[[:d = at(document.id, "WHx-gSYAAMkyXYX_")]]')\
            .submit()\
            .documents[0]
        self.assertEqual(len(doc.linked_documents), 2)

    def test_fetch_links(self):
        article = self.api\
            .form('everything')\
            .ref(self.api.get_master())\
            .fetch_links('all.text')\
            .query(predicates.at('document.id', 'WHx-gSYAAMkyXYX_')) \
            .submit()\
            .documents[0]
        links = article.get_all('all.link_document')
        self.assertEqual(links[0].get_text('all.text'), 'all1')

    def test_fetch_links_list(self):
        article = self.api\
            .form('everything')\
            .ref(self.api.get_master())\
            .fetch_links(['all.text', 'all.number'])\
            .query(predicates.at('document.id', 'WH2PaioAALYBEgug')) \
            .submit()\
            .documents[0]
        links = article.get_all('all.link_document')
        self.assertEqual(links[0].get_text('all.text'), 'all')
        self.assertEqual(links[0].get_text('all.number'), 20)


class ApiTestCase(PrismicTestCase):
    def test_get_ref_master(self):
        self.assertEqual(self.api.get_ref("Master").ref, "UgjWQN_mqa8HvPJY")

    def test_get_ref(self):
        self.assertEqual(self.api.get_ref("San Francisco Grand opening").ref, "UgjWRd_mqbYHvPJa")

    def test_get_master(self):
        self.assertEqual(self.api.get_master().ref, "UgjWQN_mqa8HvPJY")
        self.assertEqual(self.api.get_master().id, "master")


class TestSearchFormTestCase(PrismicTestCase):
    def test_document(self):
        docs = [prismic.Document(doc) for doc in self.fixture_search]
        self.assertEqual(len(docs), 3)
        doc = docs[0]
        self.assertEqual(doc.slug, "vanilla-macaron")

    def test_empty_slug(self):
        doc_json = self.fixture_search[0]
        doc_json["slugs"] = None
        doc = prismic.Document(doc_json)
        self.assertEqual(doc.slug, "-")

    def test_as_html(self):
        doc_json = self.fixture_search[0]
        doc = prismic.Document(doc_json)
        expected_html = ("""<section data-field="product.allergens"><span class="text">Contains almonds, eggs, milk</span></section>"""
                         """<section data-field="product.image"><img src="https://wroomio.s3.amazonaws.com/micro/0417110ebf2dc34a3e8b7b28ee4e06ac82473b70.png" alt="" width="500" height="500" /></section>"""
                         """<section data-field="product.short_lede"><h2>Crispiness and softness, rolled into one</h2></section>"""
                         """<section data-field="product.testimonial_author[0]"><h3>Chef Guillaume Bort</h3></section><section data-field="product.related[0]"><a href="document/UdUjvt_mqVNObPeO">dark-chocolate-macaron</a></section>"""
                         """<section data-field="product.name"><h1>Vanilla Macaron</h1></section>"""
                         """<section data-field="product.related[1]"><a href="document/UdUjsN_mqT1ObPeM">salted-caramel-macaron</a></section>"""
                         """<section data-field="product.testimonial_quote[0]"><p>The taste of pure vanilla is very hard to tame, and therefore, most cooks resort to substitutes. <strong>It takes a high-skill chef to know how to get the best of tastes, and <strong><em></strong>Les Bonnes Choses<strong></em></strong>'s vanilla macaron does just that</strong>. The result is more than a success, it simply is a gastronomic piece of art.</p></section>"""
                         """<section data-field="product.flavour[0]"><span class="text">Vanilla</span></section>"""
                         """<section data-field="product.price"><span class="number">3.55</span></section><section data-field="product.color"><span class="color">#ffeacd</span></section>"""
                         """<section data-field="product.description"><p>Experience the ultimate vanilla experience. Our vanilla Macarons are made with our very own (in-house) <strong>pure extract of Madagascar vanilla</strong>, and subtly dusted with <strong>our own vanilla sugar</strong> (which we make from real vanilla beans).</p></section>""")
        doc_html = doc.as_html(lambda link_doc: "document/%s" % link_doc.id)
        # Comparing len rather than actual strings because json loading is not in a deterministic order for now
        self.assertEqual(len(expected_html), len(doc_html))

    def test_default_params_empty(self):
        form = self.api.form("everything")
        self.assertEqual(len(form.data), 0)

    def test_query_append_value(self):
        form = self.api.form("everything")
        form.query("[[bar]]")
        self.assertEqual(len(form.data), 1)
        self.assertEqual(form.data["q"], ["[[bar]]"])

    def test_ref_replace_value(self):
        form = self.api.form("everything")
        form.ref("foo")
        self.assertEqual(len(form.data), 1)
        self.assertEqual(form.data["ref"], "foo")
        form.ref("bar")
        self.assertEqual(len(form.data), 1)
        self.assertEqual(form.data["ref"], "bar")

    def test_set_page_size(self):
        form = self.api.form("everything")
        form.page_size(3)
        self.assertEqual(len(form.data), 1)
        self.assertEqual(form.data["pageSize"], 3)

    def test_set_page(self):
        form = self.api.form("everything")
        form.page(3)
        self.assertEqual(len(form.data), 1)
        self.assertEqual(form.data["page"], 3)


class TestFragmentsTestCase(PrismicTestCase):
    def setUp(self):
        super(TestFragmentsTestCase, self).setUp()
        doc_json = self.fixture_search[0]
        self.doc = prismic.Document(doc_json)

    def test_image(self):
        doc = self.doc
        self.assertEqual(doc.get_image("product.image", "main").width, 500)
        self.assertEqual(doc.get_image("product.image", "icon").width, 250)
        expected_html = \
            ("""<img """
             """src="https://wroomio.s3.amazonaws.com/micro/babdc3421037f9af77720d8f5dcf1b84c912c6ba.png" """
             """alt="" width="250" height="250" />""")
        self.assertEqual(expected_html, doc.get_image("product.image", "icon").as_html(PrismicTestCase.link_resolver))

    def test_number(self):
        doc = self.doc
        self.assertEqual(doc.get_number("product.price").__str__(), "3.55")

    def test_color(self):
        doc = self.doc
        self.assertEqual(doc.get_color("product.color").__str__(), "#ffeacd")

    def test_text(self):
        doc = self.doc
        self.assertEqual(doc.get_text("product.allergens").__str__(), "Contains almonds, eggs, milk")

        text = prismic.Fragment.Text("a&b 42 > 41")
        self.assertEqual(text.as_html, '<span class="text">a&amp;b 42 &gt; 41</span>', "HTML escape")

    def test_structured_text_heading(self):
        doc = self.doc
        html = doc.get_html("product.short_lede", lambda x: "/x")
        self.assertEqual("<h2>Crispiness and softness, rolled into one</h2>", html)

    def test_structured_text_paragraph(self):
        span_sample_data = {"type": "paragraph",
                            "text": "To be or not to be ?",
                            "spans": [
                                {"start": 3, "end": 5, "type": "strong"},
                                {"start": 16, "end": 18, "type": "strong"},
                                {"start": 3, "end": 5, "type": "em"}
                            ]}
        p = prismic.fragments.StructuredText([span_sample_data])
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, "<p>To <em><strong>be</strong></em> or not to <strong>be</strong> ?</p>")

        p = prismic.fragments.StructuredText([{"type": "paragraph", "text": "a&b 42 > 41", "spans": []}])
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, "<p>a&amp;b 42 &gt; 41</p>", "Paragraph HTML escape")

        p = prismic.fragments.StructuredText([{"type": "heading2", "text": "a&b 42 > 41", "spans": []}])
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, "<h2>a&amp;b 42 &gt; 41</h2>", "Header HTML escape")

    def test_spans(self):
        doc_json = self.fixture_spans_labels
        p = prismic.fragments.StructuredText(doc_json.get("value"))
        p_html = p.as_html(lambda x: "/x")
        self.assertEqual(p_html, ("""<p>Two <strong><em>spans</em> with</strong> the same start</p>"""
                                  """<p>Two <em><strong>spans</strong> with</em> the same start</p>"""
                                  """<p>Span till the <span class="tip">end</span></p>"""))

    def test_lists(self):
        doc_json = self.fixture_structured_lists[0]
        doc = prismic.Document(doc_json)
        doc_html = doc.get_structured_text("article.content").as_html(lambda x: "/x")
        expected = ("""<ul><li>Element1</li><li>Element2</li><li>Element3</li></ul>"""
                    """<p>Ordered list:</p><ol><li>Element1</li><li>Element2</li><li>Element3</li></ol>""")
        self.assertEqual(doc_html, expected)

    def test_empty_paragraph(self):
        doc_json = self.fixture_empty_paragraph
        doc = prismic.Document(doc_json)

        doc_html = doc.get_field('announcement.content').as_html(PrismicTestCase.link_resolver)
        expected = """<p>X</p><p></p><p>Y</p>"""
        self.assertEqual(doc_html, expected)

    def test_block_labels(self):
        doc_json = self.fixture_block_labels
        doc = prismic.Document(doc_json)

        doc_html = doc.get_field('announcement.content').as_html(PrismicTestCase.link_resolver)
        expected = """<p class="code">some code</p>"""
        self.assertEqual(doc_html, expected)

    def test_get_text(self):
        doc_json = self.fixture_search[0]
        doc = prismic.Document(doc_json)
        self.assertEqual(doc.get_text('product.description'), 'Experience the ultimate vanilla experience. Our vanilla Macarons are made with our very own (in-house) pure extract of Madagascar vanilla, and subtly dusted with our own vanilla sugar (which we make from real vanilla beans).')

    def test_document_link(self):
        test_paragraph = {
            "type": "paragraph",
            "text": "bye",
            "spans": [
                {
                    "start": 0,
                    "end": 3,
                    "type": "hyperlink",
                    "data": {
                        "type": "Link.document",
                        "value": {
                            "document": {
                                "id": "UbiYbN_mqXkBOgE2", "type": "article", "tags": ["form"], "slug": "-"
                            },
                            "isBroken": False
                        }
                    }
                },
                {"start": 0, "end": 3, "type": "strong"}
            ]
        }
        p = prismic.fragments.StructuredText([test_paragraph])

        def link_resolver(document_link):
            return "/document/%s/%s" % (document_link.id, document_link.slug)

        p_html = p.as_html(link_resolver)
        self.assertEqual(p_html, """<p><strong><a href="/document/UbiYbN_mqXkBOgE2/-">bye</a></strong></p>""")

    def test_geo_point(self):
        store = prismic.Document(self.fixture_store_geopoint)
        geopoint = store.get_field("store.coordinates")
        self.assertEqual(geopoint.as_html,
                         ("""<div class="geopoint"><span class="latitude">37.777431</span>"""
                          """<span class="longitude">-122.415419</span></div>"""))

    def test_group(self):
        contributor = prismic.Document(self.fixture_groups)
        links = contributor.get_group("contributor.links")
        self.assertEquals(len(links.value), 2)

    def test_slicezone(self):
        self.maxDiff = 10000
        doc = prismic.Document(self.fixture_slices)
        slices = doc.get_slice_zone("article.blocks")
        slices_html = slices.as_html(PrismicTestCase.link_resolver)
        expected_html = (
            """<div data-slicetype="features" class="slice"><section data-field="illustration"><img src="https://wroomdev.s3.amazonaws.com/toto/db3775edb44f9818c54baa72bbfc8d3d6394b6ef_hsf_evilsquall.jpg" alt="" width="4285" height="709" /></section>"""
            """<section data-field="title"><span class="text">c'est un bloc features</span></section></div>\n"""
            """<div data-slicetype="text" class="slice"><p>C'est un bloc content</p></div>""")
        # Comparing len rather than actual strings because json loading is not in a deterministic order for now
        self.assertEqual(len(expected_html), len(slices_html))

    def test_composite_slices(self):
        self.maxDiff = 1000
        doc = prismic.Document(self.fixture_composite_slices)
        slices = doc.get_slice_zone("test.body")
        slices_html = slices.as_html(PrismicTestCase.link_resolver)
        expected_html = """<div data-slicetype="slice-a" class="slice"><section data-field="non-repeat-text"><p>Slice A non-repeat text</p></section><section data-field="non-repeat-title"><h1>Slice A non-repeat title</h1></section><section data-field="repeat-text"><p>Repeatable text A</p></section><section data-field="repeat-title"><h1>Repeatable title A</h1></section>
<section data-field="repeat-text"><p>Repeatable text B</p></section><section data-field="repeat-title"><h1>Repeatable title B</h1></section></div>
<div data-slicetype="slice-b" class="slice"><section data-field="image"><img src="https://prismic-io.s3.amazonaws.com/tails/014c1fe46e3ceaf04b7cc925b2ea7e8027dc607a_mobile_header_tp.png" alt="" width="800" height="500" /></section><section data-field="title"><h1>Slice A non-repeat title</h1></section></div>"""
        # Comparing len rather than actual strings because json loading is not in a deterministic order for now
        self.assertEqual(len(expected_html), len(slices_html))

    def test_image_links(self):
        self.maxDiff = 10000
        text = prismic.fragments.StructuredText(self.fixture_image_links.get('value'))

        self.assertEqual(
            text.as_html(PrismicTestCase.link_resolver),
            ("""<p>Here is some introductory text.</p>"""
             """<p>The following image is linked.</p>"""
             """<p class="block-img"><a href="http://google.com/">"""
             """<img src="http://fpoimg.com/129x260" alt="" width="260" height="129" /></a></p>"""
             """<p><strong>More important stuff</strong></p><p>The next is linked to a valid document:</p>"""
             """<p class="block-img"><a href="/document/UxCQFFFFFFFaaYAH/something-fantastic">"""
             """<img src="http://fpoimg.com/400x400" alt="" width="400" height="400" /></a></p>"""
             """<p>The next is linked to a broken document:</p><p class="block-img"><a href="#broken">"""
             """<img src="http://fpoimg.com/250x250" alt="" width="250" height="250" /></a></p>"""
             """<p>One more image, this one is not linked:</p><p class="block-img">"""
             """<img src="http://fpoimg.com/199x300" alt="" width="300" height="199" /></p>"""))

    def test_custom_html(self):
        self.maxDiff = 10000
        text = prismic.fragments.StructuredText(self.fixture_custom_html.get('value'))

        self.assertEqual(
            text.as_html(PrismicTestCase.link_resolver, PrismicTestCase.html_serializer),
            ("""<p>Here is some introductory text.</p>"""
             """<p>The following image is linked.</p>"""
             """<a href="http://google.com/"><img src="http://fpoimg.com/129x260" alt="" width="260" height="129" /></a>"""
             """<p><strong>More important stuff</strong></p><p>The next is linked to a valid document:</p>"""
             """<a href="/document/UxCQFFFFFFFaaYAH/something-fantastic">"""
             """<img src="http://fpoimg.com/400x400" alt="" width="400" height="400" /></a>"""
             """<p>The next is linked to a broken document:</p><a href="#broken">"""
             """<img src="http://fpoimg.com/250x250" alt="" width="250" height="250" /></a>"""
             """<p>One more image, this one is not linked:</p>"""
             """<img src="http://fpoimg.com/199x300" alt="" width="300" height="199" />"""
             """<p>This <a class="some-link" href="/document/UlfoxUnM0wkXYXbu/les-bonnes-chosess-internship-a-testimony">"""
             """paragraph</a> contains an hyperlink.</p>"""))


class PredicatesTestCase(PrismicTestCase):

    def test_at(self):
        f = self.api\
            .form("everything")\
            .ref(self.api.get_master())\
            .query(predicates.at('document.id', 'UlfoxUnM0wkXYXbZ'))
        self.assertEqual(f.data['q'], ["[[:d = at(document.id, \"UlfoxUnM0wkXYXbZ\")]]"])

    def test_not(self):
        f = self.api\
            .form("everything")\
            .ref(self.api.get_master())\
            .query(predicates.not_('document.id', 'UlfoxUnM0wkXYXbZ'))
        self.assertEqual(f.data['q'], ["[[:d = not(document.id, \"UlfoxUnM0wkXYXbZ\")]]"])

    def test_any(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(predicates.any('document.type', ['article', 'form-post']))
        self.assertEqual(f.data['q'], ['[[:d = any(document.type, ["article", "form-post"])]]'])

    def test_similar(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(predicates.similar('idOfSomeDocument', 10))
        self.assertEqual(f.data['q'], ['[[:d = similar("idOfSomeDocument", 10)]]'])

    def test_multiple_predicates(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(
                predicates.month_after('my.form-post.publication-date', 4),
                predicates.month_before('my.form-post.publication-date', 'December')
            )
        self.assertEqual(f.data['q'], ['[[:d = date.month-after(my.form-post.publication-date, 4)][:d = date.month-before(my.form-post.publication-date, "December")]]'])

    def test_number_lt(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(predicates.lt('my.form-post.publication-date', 4))
        self.assertEqual(f.data['q'], ['[[:d = number.lt(my.form-post.publication-date, 4)]]'])

    def test_number_in_range(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(predicates.in_range('my.product.price', 2, 4.5))
        self.assertEqual(f.data['q'], ['[[:d = number.inRange(my.product.price, 2, 4.5)]]'])

    def test_geopoint_near(self):
        f = self.api \
            .form("everything") \
            .ref(self.api.get_master()) \
            .query(predicates.near('my.store.coordinates', 40.689757, -74.0451453, 15))
        self.assertEqual(f.data['q'], ['[[:d = geopoint.near(my.store.coordinates, 40.689757, -74.0451453, 15)]]'])


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = ShelveCache("cachetest")

    def test_set_get(self):
        self.cache.set("foo", "bar", 3600)
        self.assertEqual(self.cache.get("foo"), "bar")

    def test_expiration(self):
        self.cache.set("toto", "tata", 2)
        time.sleep(3)
        self.assertIsNone(self.cache.get("toto"))


if __name__ == '__main__':
    unittest.main()
