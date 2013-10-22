#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import structured_text
import logging
import cgi

log = logging.getLogger(__name__)

class FragmentElement(object):
    pass

class Fragment(object):

    _types = None

    @classmethod
    def from_json(cls, data):
        """Create a corresponding fragment object from json."""

        if not cls._types:
            cls._types = {
                "Image":          Fragment.Image,
                "Color":          Fragment.Color,
                "Text":           Fragment.Text,
                "Select":         Fragment.Text,
                "Number":         Fragment.Number,
                "StructuredText": structured_text.StructuredText,
                "Link.document":  Fragment.DocumentLink
            }

        fragment_type = data.get("type")
        f_type = cls._types.get(fragment_type)

        if f_type:
            return f_type(data.get("value"))

        log.warning("fragment_type not found: %s" % fragment_type)


    # Links

    class Link(FragmentElement):
        pass


    class DocumentLink(Link):
        def __init__(self, value):
            document = value.get("document")

            self.id = document.get("id")
            self.type = document.get("type")
            self.tags = document.get("tags")
            self.slug = document.get("slug")
            self.is_broken = value.get("isBroken")

        def as_html(self, documentlink_resolver):
            """Get the DocumentLink as html.

            :param documentlink_resolver: A resolver function will be called with :class:`prismic.fragments.Fragment.DocumentLink <prismic.fragments.Fragment.DocumentLink>` object as argument. Resolver function should return a string, the local url to the document.
            """
            return """<a href="%(link)s">%(slug)s</a>""" % {"link": self.get_url(documentlink_resolver), "slug": self.slug}

        def get_url(self, documentlink_resolver):
            if not hasattr(documentlink_resolver, '__call__'):
                raise Exception("documentlink_resolver should be a callable object, but it's: %s" % type(documentlink_resolver))
            return documentlink_resolver(self)

        def get_document_id(self):
            return self.id

        def get_document_type(self):
            return self.type

        def get_document_tags(self):
            return self.type

        def get_document_slug(self):
            return self.type

    class WebLink(Link):
        def __init__(self, value):
            self.url = value.get("url")

        @property
        def as_html(self):
            return """<a href="%(url)s">%(url)s</a>""" % self.__dict__

        def get_url(self):
            return self.url


    class Image(FragmentElement):
        _View = namedtuple('View', ['url', 'width', 'height'])

        class View(FragmentElement, _View):
            """View class"""

            @classmethod
            def make(cls, data):
                return cls(data["url"], data["dimensions"]["width"], data["dimensions"]["height"])

            @property
            def as_html(self):
                return """<img src="%(url)s" width="%(width)s" height="%(height)s">""" % self._asdict()

            @property
            def ratio(self):
                return self.width / self.height


        def __init__(self, value):
            main, views = value.get("main"), value.get("views")

            self.main = Fragment.Image.View.make(main)
            self.views = { view_key: Fragment.Image.View.make(view_value) for (view_key, view_value) in views.iteritems() }

        def get_view(self, key):
            if key == "main":
                return self.main
            else:
                return self.views.get(key)

        @property
        def as_html(self):
            return self.main.as_html


    class Embed(FragmentElement):
        def __init__(self, value):
            oembed = value.get("oembed")
            self.type = oembed.get("type")
            self.provider = oembed.get("provider_name")
            self.provider = oembed.get("provider_name")
            self.url = oembed.get("embed_url")
            self.width = oembed.get("width")
            self.height = oembed.get("height")
            self.html = oembed.get("html")

        @property
        def as_html(self):
            return """<div data-oembed="%(url)s" data-oembed-type="%(type)s" data-oembed-provider="%(provider)s">%(html)s</div>""" % self.__dict__

    # Basic fragments

    class BasicFragment(FragmentElement):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.value.__str__()


    class Number(BasicFragment):

        @property
        def as_html(self):
            return """<span class="number">%g</span>""" % self.value


    class Color(BasicFragment):

        @property
        def as_html(self):
            return """<span class="color">%s</span>""" % self.value

    class Text(BasicFragment):

        @property
        def as_html(self):
            return """<span class="text">%s</span>""" % cgi.escape(self.value)
