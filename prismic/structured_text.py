#!/usr/bin/env python
# -*- coding: utf-8 -*-


class StructuredText(object):

    def __init__(self, values):
        self.fragments = []

        types = {
            "heading1": Heading,
            "heading2": Heading,
            "heading3": Heading,
            "heading4": Heading,
            "paragraph": Paragraph,
            "list-item": ListItem,
            "image": lambda val: Fragment.Image.View(val),
            "embed": lambda val: Fragment.Image.View(val),
        }

        for value in values:
            text_type = value.get("type")
            type_class = types.get(text_type)
            if type_class:
                self.fragments.append(type_class(value))
            else:
                print "Type not found: ", text_type
        # print "self.fragments ", self.fragments


class Block(object):

    """A block in a structured text"""
    pass


class Span(object):

    @classmethod
    def from_json(cls, data):
        if data.get("type") == "strong":
            return Span.Strong(data)
        elif data.get("type") == "em":
            return Span.Em(data)

    class SpanElement(object):

        def __init__(self, value):
            self.start = value.get("start")
            self.end = value.get("end")

    class Em(SpanElement):
        pass

    class Strong(SpanElement):
        pass

# Text


class Text(Block):

    def __init__(self, value):
        self.text = value.get("text")
        self.spans = [Span.from_json(span) for span in value.get("spans")]


class Heading(Text):

    def __init__(self, value):
        super(Heading, self).__init__(value)


class Paragraph(Text):

    def __init__(self, value):
        super(Paragraph, self).__init__(value)


class ListItem(Text):

    def __init__(self, value):
        super(ListItem, self).__init__(value)

# Other


class Embed(Block):

    def __init__(self, value):
        pass


class Image(Block):

    def __init__(self, view):
        pass