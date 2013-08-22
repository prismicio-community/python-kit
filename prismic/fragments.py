#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple


class Fragment(object):
    @staticmethod
    def make(data):
        fragment_type = data.get("type")
        if fragment_type == "Image":
            return Image(data)
        #elif fragment_type == "StructuredText":
        #    return StructuredText()

class Number(Fragment):

    def __init__(self, data):
        self.value = data.get("value")

    @property
    def as_html(self):
        return """<span class="number">%g</span>""" % self.value


class Image(Fragment):
    _View = namedtuple('View', ['url', 'width', 'height'])

    class View(_View):
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


    def __init__(self, data):
        value = data.get("value") 
        main, views = value.get("main"), value.get("views")

        self.main = Image.View.make(main)
        self.views = { view_key: Image.View.make(view_value) for (view_key,view_value) in views.iteritems() }

    def get_view(self, key):
        if key == "main":
            return self.main
        else:
            return self.views.get(key)