#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from collections import namedtuple, defaultdict
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
                "Date":           Fragment.Date,
                "StructuredText": StructuredText,
                "Link.document":  Fragment.DocumentLink,
                "Link.file":      Fragment.MediaLink,
                "Link.web":       Fragment.WebLink,
                "Embed":          Fragment.Embed,
                "GeoPoint":       Fragment.GeoPoint,
                "Group":          Fragment.Group
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

        def get_url(self, documentlink_resolver=None):
            if not hasattr(documentlink_resolver, '__call__'):
                raise Exception("documentlink_resolver should be a callable object, but it's: %s" % type(documentlink_resolver))
            return documentlink_resolver(self)

        def get_document_id(self):
            return self.id

        def get_document_type(self):
            return self.type

        def get_document_tags(self):
            return self.tags

        def get_document_slug(self):
            return self.slug

    class WebLink(Link):
        def __init__(self, value):
            self.url = value.get("url")

        @property
        def as_html(self):
            return """<a href="%(url)s">%(url)s</a>""" % self.__dict__

        def get_url(self):
            return self.url

    class MediaLink(Link):
        def __init__(self, value):
            self.file = value.get("file")
            self.url = self.file.get("url")
            self.kind = self.file.get("kind")
            self.size = self.file.get("size")
            self.name = self.file.get("name")

        def as_html(self):
            return "<a href='%(url)s'>%(name)s</a>" % self.__dict__

        def get_file(self):
            return self.file

        def get_filename(self):
            return self.name

    class Image(FragmentElement):
        _View = namedtuple('View', ['url', 'width', 'height'])

        class View(FragmentElement, _View):
            """View class"""

            @classmethod
            def make(cls, data):
                return cls(data["url"], data["dimensions"]["width"], data["dimensions"]["height"])

            @property
            def as_html(self):
                return """<img src="%(url)s" width="%(width)s" height="%(height)s">""" % {
                    'url': self.url,
                    'width': self.width,
                    'height': self.height
                }

            @property
            def ratio(self):
                return self.width / self.height

        def __init__(self, value):
            main, views = value.get("main"), value.get("views")

            self.main = Fragment.Image.View.make(main)
            self.views = {
                view_key: Fragment.Image.View.make(view_value) for (view_key, view_value) in list(views.items())
            }

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
            return ("""<div data-oembed="%(url)s" data-oembed-type="%(type)s" data-oembed-provider="%(provider)s">"""
                    "%(html)s"
                    "</div>") % self.__dict__

    class GeoPoint(FragmentElement):
        def __init__(self, value):
            self.latitude = value.get("latitude")
            self.longitude = value.get("longitude")

        @property
        def as_html(self):
            return ("""<div class="geopoint"><span class="latitude">"""
                    """%(latitude)f</span><span class="longitude">%(longitude)f</span>"""
                    """</div>""") % self.__dict__

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

    class Date(BasicFragment):

        @property
        def as_html(self):
            return """<time>%s</time>""" % self.value

    class Group(BasicFragment):
        def __init__(self, value):
            self.value = []
            for elt in value:
                group = {}
                for name, frag in elt.items():
                    group[name] = Fragment.from_json(frag)
                self.value.append(group)

        @property
        def as_html(self):
            result = ""
            for element in self.value:
                for k, v in element.items():
                    result += ("<section data-field=\"%(key)s\">%(html)s</section" %
                               {"key": k, "html": v.as_html})
            return result


class StructuredText(object):

    def __init__(self, values):
        types = {
            "heading1": Block.Heading,
            "heading2": Block.Heading,
            "heading3": Block.Heading,
            "heading4": Block.Heading,
            "paragraph": Block.Paragraph,
            "list-item": Block.ListItem,
            "o-list-item": lambda val: Block.ListItem(val, True),
            "image": lambda val: Block.Image(Fragment.Image.View.make(val)),
            "embed": lambda val: Block.Embed(Fragment.Embed(val)),
        }

        blocks = []

        for value in values:
            text_type = value.get("type")
            type_class = types.get(text_type)
            if type_class:
                blocks.append(type_class(value))
            else:
                log.warning("StructuredText, type not found: %s" % text_type)

        self.blocks = blocks

    def get_title(self):
        return next(p for p in self.blocks if isinstance(p, Block.Heading))

    def get_first_paragraph(self):
        return next(p for p in self.blocks if isinstance(p, Block.Paragraph))

    def get_image(self):
        return next(p for p in self.blocks if isinstance(p, Block.Image))

    class Group(object):
        def __init__(self, tag, blocks):
            self.tag = tag
            self.blocks = blocks

    def as_html(self, link_resolver):
        groups = []
        for block in self.blocks:
            if len(groups) > 0:
                last_one = groups[-1:][0]

                if last_one.tag == "ul" and isinstance(block, Block.ListItem) and not block.is_ordered:
                    last_one.blocks.append(block)
                elif last_one.tag == "ol" and isinstance(block, Block.ListItem) and block.is_ordered:
                    last_one.blocks.append(block)
                elif isinstance(block, Block.ListItem) and not block.is_ordered:
                    groups.append(StructuredText.Group("ul", [block]))
                elif isinstance(block, Block.ListItem) and block.is_ordered:
                    groups.append(StructuredText.Group("ol", [block]))
                else:
                    groups.append(StructuredText.Group(None, [block]))
            else:
                groups.append(StructuredText.Group(None, [block]))

        html = []
        for group in groups:
            if group.tag is not None:
                html.append("<%(tag)s>" % group.__dict__)
                for block in group.blocks:
                    html.append(StructuredText.block_as_html(block, link_resolver))
                html.append("</%(tag)s>" % group.__dict__)
            else:
                for block in group.blocks:
                    html.append(StructuredText.block_as_html(block, link_resolver))

        html_str = ''.join(html)
        log.debug("as_html result: %s" % html_str)
        return html_str

    @staticmethod
    def block_as_html(block, link_resolver):
        if isinstance(block, Block.Heading):
            return "<h%(level)s>%(html)s</h%(level)s>" % \
                   {"level": block.level, "html": StructuredText.span_as_html(block.text, block.spans, link_resolver)}
        elif isinstance(block, Block.Paragraph):
            return "<p>%s</p>" % StructuredText.span_as_html(block.text, block.spans, link_resolver)
        elif isinstance(block, Block.ListItem):
            return "<li>%s</li>" % StructuredText.span_as_html(block.text, block.spans, link_resolver)
        elif isinstance(block, Block.Image):
            return "<p>%s</p>" % block.get_view().as_html
        elif isinstance(block, Block.Embed):
            return block.get_embed().as_html

    @staticmethod
    def span_write_tag(span, link_resolver, opening):
        if isinstance(span, Span.Em):
            return "<em>" if opening else "</em>"
        elif isinstance(span, Span.Strong):
            return "<strong>" if opening else "</strong>"
        elif isinstance(span, Span.Hyperlink):
            return """<a href="%s">""" % span.get_url(link_resolver) if opening else "</a>"

    @staticmethod
    def span_as_html(text, spans, link_resolver):
        html = []
        tags_map = defaultdict(list)
        for span in spans:
            tags_map[span.start].append(StructuredText.span_write_tag(span, link_resolver, True))

        for span in reversed(spans):
            tags_map[span.end].append(StructuredText.span_write_tag(span, link_resolver, False))

        index = 0
        for index, letter in enumerate(text):
            tags = tags_map.get(index)
            if tags:
                html.append(''.join(tags))
            html.append(cgi.escape(letter))

        # Check for the tags after the end of the string
        tags = tags_map.get(index + 1)
        if tags:
            html.append(''.join(tags))

        return ''.join(html)


class Span(object):

    @classmethod
    def from_json(cls, data):
        return {
            "strong": Span.Strong,
            "em": Span.Em,
            "hyperlink": Span.Hyperlink
        }.get(data.get("type"), lambda x: None)(data)

    class SpanElement(object):

        def __init__(self, value):
            self.start = value.get("start")
            self.end = value.get("end")

    class Em(SpanElement):
        pass

    class Strong(SpanElement):
        pass

    class Hyperlink(SpanElement):
        def __init__(self, value):
            super(Span.Hyperlink, self).__init__(value)
            data = value.get("data")
            hyperlink_type = data.get("type")
            self.link = {
                "Link.web": Fragment.WebLink,
                "Link.document": Fragment.DocumentLink
            }.get(hyperlink_type, lambda x: None)(data.get("value"))
            if self.link is None:
                log.warning("StructuredText::Span::Hyperlink type not found: %s" % hyperlink_type)

        def get_url(self, link_resolver):
            if isinstance(self.link, Fragment.DocumentLink):
                return self.link.get_url(link_resolver)
            elif isinstance(self.link, Fragment.WebLink):
                return self.link.get_url()


class Text(object):
    """Base class for blocks"""
    def __init__(self, value):
        self.text = value.get("text")
        self.spans = [Span.from_json(span) for span in value.get("spans")]


class Block(object):

    """A block in a structured text"""
    pass

    class Heading(Text):

        def __init__(self, value):
            super(Block.Heading, self).__init__(value)
            self.level = value.get("type")[-1]

    class Paragraph(Text):

        def __init__(self, value):
            super(Block.Paragraph, self).__init__(value)

    class ListItem(Text):

        def __init__(self, value, is_ordered=False):
            super(Block.ListItem, self).__init__(value)
            self.is_ordered = is_ordered

    class Embed(object):

        def __init__(self, embed):
            self.obj = embed

        def get_embed(self):
            return self.obj

    class Image(object):
        """Block image

        :param view: The Fragment.Image.View object
        """
        def __init__(self, view):
            self.view = view

        def get_view(self):
            return self.view