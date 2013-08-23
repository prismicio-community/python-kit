#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from .structured_text import StructuredText

class FragmentElement(object):
    pass

class Fragment(object):

    _types = None

    @classmethod
    def from_json(cls, data):
        """Create a corresponding fragment object from json."""

        if not cls._types:
            types = [Fragment.Image, Fragment.Color, Fragment.Number, Fragment.Text, StructuredText]
            cls._types = { f_type.__name__: f_type for f_type in types }
            cls._types["Link.document"] = Fragment.DocumentLink

        fragment_type = data.get("type")
        f_type = cls._types.get(fragment_type)

        if f_type:
            return f_type(data.get("value"))

        print "fragment_type not found: ", fragment_type


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

        def as_html(self, documentLinkResolver):
            return """<a href="%{link}s">%{slug}s</a>""" % {"link": documentLinkResolver, "slug": self.slug}


    class WebLink(Link):
        def __init__(self, value):
            self.url = value.get("url")

        @property
        def as_html(self):
            return """<a href="%(url)s">%(url)s</a>""" % self.__dic__


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
            self.views = { view_key: Fragment.Image.View.make(view_value) for (view_key,view_value) in views.iteritems() }

        def get_view(self, key):
            if key == "main":
                return self.main
            else:
                return self.views.get(key)

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
            return """<span class="color">%g</span>""" % self.value

    class Text(BasicFragment):

        @property
        def as_html(self):
            return """<span class="text">%g</span>""" % self.value