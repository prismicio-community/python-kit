#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from collections import namedtuple, defaultdict, OrderedDict
import logging
import cgi
import re
import datetime

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
                "Range":          Fragment.Range,
                "Date":           Fragment.Date,
                "Timestamp":      Fragment.Timestamp,
                "StructuredText": StructuredText,
                "Link.document":  Fragment.DocumentLink,
                "Link.file":      Fragment.MediaLink,
                "Link.web":       Fragment.WebLink,
                "Link.image":     Fragment.ImageLink,
                "Embed":          Fragment.Embed,
                "GeoPoint":       Fragment.GeoPoint,
                "Group":          Fragment.Group,
                "SliceZone":      Fragment.SliceZone
            }

        fragment_type = data.get("type")
        f_type = cls._types.get(fragment_type)

        if f_type:
            return f_type(data.get("value"))

        log.warning("fragment_type not found: %s" % fragment_type)

    class WithFragments(object):

        def __init__(self, fragments):
            self.fragments = fragments

        def get(self, field):
            return self.fragments.get(field, None)

        def get_field(self, field):
            return self.fragments.get(field, None)

        def get_all(self, field):
            indexed_key = "^%s(\[\d+\])?$" % field
            return list(v for k, v in list(self.fragments.items()) if re.match(indexed_key, k))

        def get_fragment_type(self, field, f_type):
            fragment = self.fragments.get(field)
            return fragment if isinstance(fragment, f_type) else None

        def get_image(self, field, view="main"):
            fragment = self.get_field(field)
            if isinstance(fragment, Fragment.Image):
                return fragment.get_view(view) if fragment else None
            if view == "main" and isinstance(fragment, StructuredText):
                image = fragment.get_image()
                return image.view if image else None
            return None

        def get_number(self, field):
            return self.get_fragment_type(field, Fragment.Number)

        def get_range(self, field):
            return self.get_fragment_type(field, Fragment.Range)

        def get_color(self, field):
            return self.get_fragment_type(field, Fragment.Color)

        def get_text(self, field):
            fragment = self.fragments.get(field)
            if isinstance(fragment, StructuredText):
                texts = [block.text for block in fragment.blocks if isinstance(
                    block, Text)]
                return "\n".join(texts) if texts else None
            elif fragment is None:
                return None
            else:
                return fragment.value

        def get_link(self, field):
            return self.get_fragment_type(field, Fragment.Link)

        def get_embed(self, field):
            return self.get_fragment_type(field, Fragment.Embed)

        def get_date(self, field):
            return self.get_fragment_type(field, Fragment.Date)

        def get_timestamp(self, field):
            return self.get_fragment_type(field, Fragment.Timestamp)

        def get_geopoint(self, field):
            return self.get_fragment_type(field, Fragment.GeoPoint)

        def get_group(self, field):
            return self.get_fragment_type(field, Fragment.Group)

        def get_structured_text(self, field):
            return self.get_fragment_type(field, StructuredText)

        def get_slice_zone(self, field):
            return self.get_fragment_type(field, Fragment.SliceZone)

        def get_html(self, field, link_resolver):
            """Get the html of a field.

            :param field: String with a name of the field to get.
            :param link_resolver: A resolver function for document links.
            Will be called with :class:`prismic.fragments.Fragment.DocumentLink <prismic.fragments.Fragment.DocumentLink>`
            object as argument. Resolver function should return a string, the local url to the document.
            """
            fragment = self.fragments.get(field)
            return self.fragment_to_html(fragment, link_resolver)

        @property
        def linked_documents(self):
            """
            Return the documents linked from this document's fragments
            :return: array<DocumentLink>
            """
            result = []
            for (name, fragment) in list(self.fragments.items()):
                if isinstance(fragment, Fragment.DocumentLink):
                    result.append(fragment)
                elif isinstance(fragment, Fragment.Group):
                    for groupdoc in fragment.value:
                        result = result + groupdoc.linked_documents
                elif isinstance(fragment, StructuredText):
                    for block in fragment.blocks:
                        if isinstance(block, Text):
                            for span in block.spans:
                                if isinstance(span, Span.Hyperlink):
                                    if isinstance(span.link, Fragment.DocumentLink):
                                        result.append(span.link)
            return result

        @staticmethod
        def fragment_to_html(fragment, link_resolver, html_serializer=None):
            if isinstance(fragment, StructuredText):
                return fragment.as_html(link_resolver, html_serializer)
            if isinstance(fragment, Fragment.Group)\
                    or isinstance(fragment, Fragment.SliceZone)\
                    or isinstance(fragment, Fragment.DocumentLink)\
                    or isinstance(fragment, Fragment.Image)\
                    or isinstance(fragment, Fragment.Image.View):
                return fragment.as_html(link_resolver)
            elif fragment:
                return fragment.as_html
            return None

        def as_html(self, link_resolver):
            html = []
            for key, fragment in list(self.fragments.items()):
                html.append("""<section data-field="%s">""" % key)
                html.append(self.fragment_to_html(fragment, link_resolver))
                html.append("""</section>""")

            return ''.join(html)

        def __getitem__(self, name):
            return self.fragments[name]

        def __iter__(self):
            return iter(self.fragments)

        def keys(self):
            return self.fragments.keys()

        def items(self):
            return self.fragments.items()

        def values(self):
            return self.fragments.values()

    # Links

    class Link(FragmentElement):

        @staticmethod
        def parse(data):
            if data is None:
                return None
            hyperlink_type = data.get("type")
            return {
                "Link.web": Fragment.WebLink,
                "Link.document": Fragment.DocumentLink,
                "Link.image": Fragment.MediaLink,
                "Link.file": Fragment.FileLink
            }.get(hyperlink_type, lambda x: None)(data.get("value"))

    class DocumentLink(WithFragments, Link):
        def __init__(self, value):
            Fragment.WithFragments.__init__(self, OrderedDict())

            document = value.get("document")

            self.id = document.get("id")
            self.uid = document.get("uid")
            self.type = document.get("type")
            self.tags = document.get("tags")
            self.slug = document.get("slug")
            self.is_broken = value.get("isBroken")

            fragments = document.get("data").get(self.type) if "data" in document else {}
            for (fragment_name, fragment_value) in list(fragments.items()):
                f_key = "%s.%s" % (self.type, fragment_name)

                if isinstance(fragment_value, list):
                    for index, fragment_value_element in enumerate(fragment_value):
                        self.fragments["%s[%s]" % (f_key, index)] = Fragment.from_json(
                            fragment_value_element)

                elif isinstance(fragment_value, dict):
                    self.fragments[f_key] = Fragment.from_json(fragment_value)

        def as_html(self, documentlink_resolver, html_serializer=None):
            """Get the DocumentLink as html.

            :param documentlink_resolver: A resolver function will be called with
            :class:`prismic.fragments.Fragment.DocumentLink <prismic.fragments.Fragment.DocumentLink>` object as
            argument. Resolver function should return a string, the local url to the document.
            """
            return """<a href="%(link)s">%(slug)s</a>""" % {
                "link": self.get_url(documentlink_resolver),
                "slug": self.slug
            }

        def get_url(self, documentlink_resolver=None):
            if not hasattr(documentlink_resolver, '__call__'):
                raise Exception(
                    "documentlink_resolver should be a callable object, but it's: %s"
                    % type(documentlink_resolver)
                )
            return documentlink_resolver(self)

        def get_document_id(self):
            return self.id

        def get_document_type(self):
            return self.type

        def get_document_tags(self):
            return self.tags

        def get_document_slug(self):
            return self.slug

        def __repr__(self):
            return "DocumentLink %s, %s, %s, %s" % (self.id, self.type, self.tags, self.is_broken)

    class WebLink(Link):
        def __init__(self, value):
            self.url = value.get("url")

        @property
        def as_html(self):
            return """<a href="%(url)s">%(url)s</a>""" % self.__dict__

        def get_url(self, link_resolver=None):
            return self.url

    class MediaLink(Link):
        def __init__(self, value):
            self.image = value.get("image")
            self.name = self.image.get("name")
            self.kind = self.image.get("kind")
            self.url = self.image.get("url")
            self.size = self.image.get("size")
            self.height = self.image.get("height")
            self.width = self.image.get("width")

        def as_html(self):
            return "<a href='%(url)s'>%(name)s</a>" % self.__dict__

        def get_url(self, link_resolver=None):
            return self.url

    class FileLink(Link):
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

        def get_url(self, link_resolver=None):
            return self.url

    class ImageLink(Link):
        def __init__(self, value):
            self.image = value.get("image")
            self.url = self.image.get("url")
            self.alt = self.image.get("alt", "")

        @property
        def as_html(self):
                return """<a href="%(url)s"><img src="%(url)s" alt="%(alt)s"/></a>""" % self.__dict__

        def get_image(self):
                return self.image

        def get_url(self):
                return self.url

    class Image(FragmentElement):
        _View = namedtuple('View', ['url', 'width', 'height', 'linkTo'])

        class View(FragmentElement):
            """View class"""

            def __init__(self, data):
                self.url = data["url"]
                self.width = data["dimensions"]["width"]
                self.height = data["dimensions"]["height"]
                self.alt = data.get("alt")
                self.copyright = data.get("copyright")
                self.link_to = Fragment.Link.parse(data.get("linkTo"))
                self.label = data.get("label")

            def as_html(self, link_resolver):
                img_tag = """<img src="%(url)s" alt="%(alt)s" width="%(width)s" height="%(height)s" />""" % {
                    'url': self.url,
                    'width': self.width,
                    'height': self.height,
                    'alt': self.alt if (self.alt is not None) else ""
                }
                if self.link_to is None:
                    return img_tag
                else:
                    url = self.link_to.get_url(link_resolver)
                    return """<a href="%(url)s">%(content)s</a>""" % {
                        'url': url,
                        'content': img_tag
                    }

            @property
            def ratio(self):
                return self.width / self.height

        def __init__(self, value):
            main, views, link = value.get("main"), value.get("views"), value.get("linkTo")

            self.main = Fragment.Image.View(main)
            self.views = {
                view_key: Fragment.Image.View(view_value) for (view_key, view_value) in list(views.items())
            }
            self.link_to = Fragment.Link.parse(link)

        def get_view(self, key):
            if key == "main":
                return self.main
            else:
                return self.views.get(key)

        def as_html(self, link_resolver):
            view_html = self.main.as_html(link_resolver)
            if self.link_to is None:
                return view_html
            else:
                return """<a href="%(url)s">%(content)s</a>""" % {
                    'url': self.link_to.get_url(link_resolver),
                    'content': view_html
                }

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

    class Range(BasicFragment):

        @property
        def as_html(self):
            return """<span class="range">%s</span>""" % self.value

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
        def as_datetime(self):
            return datetime.datetime(*map(int, re.split('[^\d]', self.value)))

        @property
        def as_html(self):
            return """<time>%s</time>""" % self.value

    class Timestamp(BasicFragment):

        @property
        def as_datetime(self):
            return datetime.datetime(*map(int, re.split('[^\d]', self.value)))

        @property
        def as_html(self):
            return """<time>%s</time>""" % self.value

    class Group(BasicFragment):

        def __init__(self, value):
            self.value = []
            for elt in value:
                fragments = OrderedDict()
                for name, frag in elt.items():
                    fragments[name] = Fragment.from_json(frag)
                self.value.append(Fragment.WithFragments(fragments))

        def as_html(self, link_resolver):
            html = []
            for group_doc in self.value:
                html.append(group_doc.as_html(link_resolver))
            return "\n".join(html)

        def __iter__(self):
            return iter(self.value)

    class Slice(FragmentElement):

        def __init__(self, slice_type, slice_label, value):
            self.slice_type = slice_type
            self.slice_label = slice_label
            self.value = value

        def as_html(self, link_resolver):
            classes = ['slice']
            if self.slice_label is not None:
                classes.append(self.slice_label)
            return '<div data-slicetype="%(slice_type)s" class="%(classes)s">%(body)s</div>' % {
                "slice_type": self.slice_type,
                "classes": ' '.join(classes),
                "body": self.value.as_html(link_resolver)
            }

    class CompositeSlice(FragmentElement):

        def __init__(self, slice_type, slice_label, elt):
            self.slice_type = slice_type
            self.slice_label = slice_label
            self.repeat = []
            self.non_repeat = {}

            _repeat = elt.get('repeat')
            _non_repeat = elt.get('non-repeat')

            if any(_repeat):
                self.repeat = self.parse_repeat(_repeat)

            if _non_repeat:
                self.non_repeat = self.parse_non_repeat(_non_repeat)

        @staticmethod
        def parse_repeat(repeat):
            return Fragment.Group(repeat)

        @staticmethod
        def parse_non_repeat(non_repeat):
            return Fragment.Group([non_repeat])

        def as_html(self, link_resolver):
            classes = ['slice']
            if self.slice_label:
                classes.append(self.slice_label)

            body = ""
            if self.non_repeat:
                body += self.non_repeat.as_html(link_resolver)

            if self.repeat:
                body += self.repeat.as_html(link_resolver)

            return '<div data-slicetype="%(slice_type)s" class="%(classes)s">%(body)s</div>' % {
                "slice_type": self.slice_type,
                "classes": ' '.join(classes),
                "body": body
            }

    class SliceZone(FragmentElement):

        def __init__(self, value):
            self.slices = []
            for elt in value:
                slice_type = elt['slice_type']
                slice_label = elt.get('slice_label')

                # Old style slice
                if 'value' in elt:
                    fragment = Fragment.from_json(elt['value'])
                    self.slices.append(Fragment.Slice(slice_type, slice_label, fragment))
                else:
                    Fragment.CompositeSlice(slice_type, slice_label, elt)
                    self.slices.append(Fragment.CompositeSlice(slice_type, slice_label, elt))

        def as_html(self, link_resolver):
            html = []
            for slice in self.slices:
                html.append(slice.as_html(link_resolver))
            return "\n".join(html)

        def __iter__(self):
            return iter(self.slices)


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
            "image": lambda val: Block.Image(Fragment.Image.View(val)),
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

    def as_html(self, link_resolver, html_serializer=None):
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
                if isinstance(block, Block.ListItem) and not block.is_ordered:
                    groups.append(StructuredText.Group("ul", [block]))
                elif isinstance(block, Block.ListItem) and block.is_ordered:
                    groups.append(StructuredText.Group("ol", [block]))
                else:
                    groups.append(StructuredText.Group(None, [block]))

        html = []
        for group in groups:
            if group.tag is not None:
                html.append("<%(tag)s>" % group.__dict__)
            for block in group.blocks:
                content = ""
                if isinstance(block, Text):
                    content = StructuredText.span_as_html(block.text, block.spans, link_resolver, html_serializer)
                html.append(StructuredText.block_as_html(block, content, link_resolver, html_serializer))
            if group.tag is not None:
                html.append("</%(tag)s>" % group.__dict__)

        html_str = ''.join(html)
        log.debug("as_html result: %s" % html_str)
        return html_str

    @staticmethod
    def block_as_html(block, content, link_resolver, html_serializer):
        if html_serializer is not None:
            custom_html = html_serializer(block, content)
            if custom_html is not None:
                return custom_html
        cls = ""
        if isinstance(block, Text) and block.label is not None:
            cls = " class=\"%s\"" % block.label
        if isinstance(block, Block.Heading):
            return "<h%(level)s%(cls)s>%(html)s</h%(level)s>" % {
                "level": block.level,
                "cls": cls,
                "html": content
            }
        elif isinstance(block, Block.Paragraph):
            return "<p%s>%s</p>" % (cls, content)
        elif isinstance(block, Block.ListItem):
            return "<li%s>%s</li>" % (cls, content)
        elif isinstance(block, Block.Image):
            all_classes = ["block-img"]
            if block.view.label is not None:
                all_classes.append(block.view.label)
            return "<p class=\"%s\">%s</p>" % (" ".join(all_classes), block.get_view().as_html(link_resolver))
        elif isinstance(block, Block.Embed):
            return block.get_embed().as_html

    @staticmethod
    def span_write_tag(span, content, link_resolver, html_serializer):
        if html_serializer is not None:
            custom_html = html_serializer(span, content)
            if custom_html is not None:
                return custom_html
        if isinstance(span, Span.Em):
            return "<em>" + content + "</em>"
        elif isinstance(span, Span.Strong):
            return "<strong>" + content + "</strong>"
        elif isinstance(span, Span.Hyperlink):
            return """<a href="%s">""" % span.get_url(link_resolver) + content + "</a>"
        else:
            cls = ""
            if span.label is not None:
                cls = " class=\"%s\"" % span.label
            return """<span%s>%s</span>""" % (cls, content)

    @staticmethod
    def span_as_html(text, spans, link_resolver, html_serializer):
        html = []
        tags_start = defaultdict(list)
        tags_end = defaultdict(list)
        for span in spans:
            tags_start[span.start].append(span)

        for span in reversed(spans):
            tags_end[span.end].append(span)

        index = 0
        stack = []
        for index, letter in enumerate(text):
            if index in tags_end:
                for end_tag in tags_end.get(index):
                    # Close a tag
                    tag = stack.pop()
                    inner_html = StructuredText.span_write_tag(tag["span"], tag["content"], link_resolver, html_serializer)
                    if len(stack) == 0:
                        # The tag was top-level
                        html.append(inner_html)
                    else:
                        # Add the content to the parent tag
                        stack[-1]["content"] += inner_html
            if index in tags_start:

                for span in reversed(sorted(tags_start.get(index), key=lambda s: s.length())):
                    # Open a tag
                    stack.append({
                        "span": span,
                        "content": ""
                    })
            if len(stack) == 0:
                # Top-level text
                html.append(cgi.escape(letter))
            else:
                # Inner text of a span
                stack[-1]["content"] += cgi.escape(letter)

        # Check for the tags after the end of the string
        while len(stack) > 0:
            # Close a tag
            tag = stack.pop()
            inner_html = StructuredText.span_write_tag(tag["span"], tag["content"], link_resolver, html_serializer)
            if len(stack) == 0:
                # The tag was top-level
                html.append(inner_html)
            else:
                # Add the content to the parent tag
                stack[-1]["content"] += inner_html

        return ''.join(html)


class Span(object):

    @classmethod
    def from_json(cls, data):
        return {
            "strong": Span.Strong,
            "em": Span.Em,
            "hyperlink": Span.Hyperlink
        }.get(data.get("type"), Span.SpanElement)(data)

    class SpanElement(object):

        def __init__(self, value):
            self.start = value.get("start")
            self.end = value.get("end")
            if value.get("data") is not None:
                self.label = value.get("data").get("label")
            else:
                self.label = None

        def length(self):
            return self.end - self.start

    class Em(SpanElement):
        pass

    class Strong(SpanElement):
        pass

    class Hyperlink(SpanElement):
        def __init__(self, value):
            super(Span.Hyperlink, self).__init__(value)
            data = value.get('data')
            self.link = Fragment.Link.parse(data)
            if self.link is None:
                log.warning("StructuredText::Span::Hyperlink type not found: %s" % data.get('type'))

        def get_url(self, link_resolver):
            return self.link.get_url(link_resolver)


class Text(object):
    """Base class for blocks"""
    def __init__(self, value):
        self.text = value.get("text")
        self.spans = [Span.from_json(span) for span in value.get("spans")]
        self.label = value.get("label")


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
