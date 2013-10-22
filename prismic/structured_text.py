#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
import fragments
import cgi

log = logging.getLogger(__name__)


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
            "image": lambda val: Block.Image(fragments.Fragment.Image.View.make(val)),
            "embed": lambda val: Block.Embed(fragments.Fragment.Embed(val)),
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


    class Group(object):
        def __init__(self, tag, blocks):
            self.tag = tag
            self.blocks = blocks

    def as_html(self, link_resolver):
        groups = []
        for block in self.blocks:
            if len(groups) > 0:
                lastOne = groups[-1:][0]

                if lastOne.tag == "ul" and isinstance(block, Block.ListItem) and not block.is_ordered:
                    lastOne.blocks.append(block)
                elif lastOne.tag == "ol" and isinstance(block, Block.ListItem) and block.is_ordered:
                    lastOne.blocks.append(block)
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
                    html.append(self.block_as_html(block, link_resolver))
                html.append("</%(tag)s>" % group.__dict__)
            else:
                for block in group.blocks:
                    html.append(self.block_as_html(block, link_resolver))

        html_str = ''.join(html)
        log.debug("as_html result: %s" % html_str)
        return html_str


    def block_as_html(self, block, link_resolver):
        if isinstance(block, Block.Heading):
            return "<h%(level)s>%(html)s</h%(level)s>" % \
                    {"level": block.level, "html": self.span_as_html(block.text, block.spans, link_resolver)} 
        elif isinstance(block, Block.Paragraph):
            return "<p>%s</p>" % self.span_as_html(block.text, block.spans, link_resolver)
        elif isinstance(block, Block.ListItem):
            return "<li>%s</li>" % self.span_as_html(block.text, block.spans, link_resolver)
        elif isinstance(block, Block.Image):
            return "<p>%s</p>" % block.get_view().as_html
        elif isinstance(block, Block.Embed):
            return block.get_embed().as_html

    def span_write_tag(self, span, link_resolver, opening):
        if isinstance(span, Span.Em):
            return "<em>" if opening else "</em>"
        elif isinstance(span, Span.Strong):
            return "<strong>" if opening else "</strong>"
        elif isinstance(span, Span.Hyperlink):
            return """<a href="%s">""" % span.get_url(link_resolver) if opening else "</a>"

    def span_as_html(self, text, spans, link_resolver):
        html = []
        tags_map = defaultdict(list)
        for span in spans:
            tags_map[span.start].append(self.span_write_tag(span, link_resolver, True))

        for span in reversed(spans):
            tags_map[span.end].append(self.span_write_tag(span, link_resolver, False))

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
        if data.get("type") == "strong":
            return Span.Strong(data)
        elif data.get("type") == "em":
            return Span.Em(data)
        elif data.get("type") == "hyperlink":
            return Span.Hyperlink(data)

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
            if hyperlink_type == "Link.web":
                self.link = fragments.Fragment.WebLink(data.get("value"))
            elif hyperlink_type == "Link.document":
                self.link = fragments.Fragment.DocumentLink(data.get("value"))
            else:
                log.warning("StructuredText::Span::Hyperlink type not found: %s" % hyperlink_type)

        def get_url(self, link_resolver):
            if isinstance(self.link, fragments.Fragment.DocumentLink):
                return self.link.get_url(link_resolver)
            elif isinstance(self.link, fragments.Fragment.WebLink):
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
