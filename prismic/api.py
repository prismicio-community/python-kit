# -*- coding: utf-8 -*-

"""
prismic.api
~~~~~~~~~~~

This module implements the Prismic API.

"""

import urllib2
from core import GenericWSRequest
from .exceptions import (InvalidTokenError, AuthorizationNeededError,
                         HTTPError, UnexpectedError, RefMissing)
from .fragments import Fragment
import structured_text
import logging

log = logging.getLogger(__name__)


def get(url, access_token):
    """Fetches the prismic api JSON.
    Returns :class:`Api <Api>` object.

    :param url: URL to the api of the repository.
    :param access_token: The access token.
    """
    try:
        request = GenericWSRequest(url)
        request.set_access_token(access_token)
        return Api(request.get_json(), access_token)

    except urllib2.HTTPError as http_error:
        if http_error.code == 401:
            if len(access_token) == 0:
                raise AuthorizationNeededError()
            else:
                raise InvalidTokenError()
        else:
            raise HTTPError(http_error.code, str(http_error))

    except urllib2.URLError as url_error:
        raise UnexpectedError("Unexpected error: %s" % url_error.reason)


class Api(object):

    def __init__(self, data, access_token):
        self.refs = [Ref(ref) for ref in data.get("refs")]
        self.bookmarks = data.get("bookmarks")
        self.types = data.get("types")
        self.tags = data.get("tags")
        self.forms = data.get("forms")
        for name in self.forms:
            form = self.forms[name]
            fields = form.get("fields")
            for field in fields:
                if field == "q":
                    fields[field].update({"multiple": True})
        self.oauth_initiate = data.get("oauth_initiate")
        self.oauth_token = data.get("oauth_token")
        self.access_token = access_token

        self.master = ([ref for ref in self.refs if ref.isMasterRef][:1] or [None])[0]
        if not self.master:
            log.error("No master reference found")

    def get_ref(self, label):
        """Get the :class:`Ref <Ref>` with a specific label.
        Returns :class:`Ref <Ref>` object.

        :param label: Name of the label.
        """
        ref = [ref for ref in self.refs if ref.label == label]
        return ref[0] if ref else None

    def get_master(self):
        """Returns current master :class:`Ref <Ref>` object."""
        return self.master

    def form(self, name):
        """Constructs the form with data from Api.
        Returns :class:`SearchForm <SearchForm>` object.

        :param name: Name of the form.
        """
        form = self.forms.get(name)
        if form is None:
            raise Exception("Bad form name %s, valid form names are: %s" % (name, ', '.join(self.forms)) )
        return SearchForm(self.forms.get(name), self.access_token)


class Ref(object):

    def __init__(self, data):
        self.ref = data.get("ref")
        self.label = data.get("label")
        self.isMasterRef = data.get("isMasterRef")
        self.scheduledAt = data.get("scheduledAt")


class SearchForm(object):

    """Form to search for documents.

    Most of the methods return self object to allow chaining.
    """

    def __init__(self, form, access_token):
        self.action = form.get("action")
        self.method = form.get("method")
        self.enctype = form.get("enctype")
        self.fields = form.get("fields") or {}
        self.data = {}
        # default values
        for field, value in self.fields.iteritems():
            if value.get("default"):
                self.set(field, value["default"])
        self.access_token = access_token

    def ref(self, ref):
        """:param ref: An :class:`Ref <Ref>` object or an string."""

        if isinstance(ref, Ref):
            ref = ref.ref

        return self.set('ref', ref)

    def query(self, query):
        return self.set('q', query)

    def set(self, field, value):
        form_field = self.fields.get(field)
        if form_field and form_field.get("multiple"):
            if not self.data.get(field):
                self.data.update({field: []})
            self.data[field].append(value)
        else:
            self.data.update({field: value})
        return self

    def submit_assert_preconditions(self):
        if (self.data.get('ref') is None):
            raise RefMissing()

    def submit(self):
        self.submit_assert_preconditions()
        request = GenericWSRequest(self.action)
        request.set_get_params(self.data)
        request.set_access_token(self.access_token)

        return [Document(doc) for doc in request.get_json()]


class Document(object):

    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")
        self.href = data.get("href")
        self.tags = data.get("tags")
        self.slugs = data.get("slugs")
        self.fragments = {}

        fragments = data.get("data").get(self.type) if "data" in data else {}

        for (fragment_name, fragment_value) in fragments.iteritems():
            f_key = "%s.%s" % (self.type, fragment_name)

            if isinstance(fragment_value, list):
                for index, fragment_value_element in enumerate(fragment_value):
                    self.fragments["%s[%s]" % (f_key, index)] = Fragment.from_json(
                        fragment_value_element)

            elif isinstance(fragment_value, dict):
                self.fragments[f_key] = Fragment.from_json(fragment_value)

    @property
    def slug(self):
        return self.slugs[0] if self.slugs else "-"

    def get_fragment_type(self, field, f_type):
        fragment = self.fragments.get(field)
        return fragment if isinstance(fragment, f_type) else None

    def get_image(self, field, view="main"):
        image = self.get_fragment_type(field, Fragment.Image)
        return image.get_view(view) if image else None

    def get_number(self, field):
        return self.get_fragment_type(field, Fragment.Number)

    def get_color(self, field):
        return self.get_fragment_type(field, Fragment.Color)

    def get_text(self, field):
        fragment = self.fragments.get(field)
        if isinstance(fragment, structured_text.StructuredText):
            texts = [block.text for block in fragment.blocks if isinstance(
                block, structured_text.Text)]
            return "\n".join(texts) if texts else None
        else:
            return fragment.value

    def get_structured_text(self, field):
        return self.get_fragment_type(field, structured_text.StructuredText)

    def get_html(self, field, link_resolver):
        """Get the html of a field.

        :param field: String with a name of the field to get.
        :param link_resolver: A resolver function for document links. It will be called with :class:`prismic.fragments.Fragment.DocumentLink <prismic.fragments.Fragment.DocumentLink>` object as argument. Resolver function should return a string, the local url to the document.
        """
        fragment = self.fragments.get(field)
        return self.fragment_to_html(fragment, link_resolver)

    def fragment_to_html(self, fragment, link_resolver):
        if (isinstance(fragment, structured_text.StructuredText) or
            isinstance(fragment, Fragment.DocumentLink)):
            return fragment.as_html(link_resolver)
        elif fragment:
            return fragment.as_html
        return None

    def as_html(self, link_resolver):
        html = []
        for key, fragment in self.fragments.items():
            html.append("""<section data-field="%s">""" % key)
            html.append(self.fragment_to_html(fragment, link_resolver))
            html.append("""</section>""")

        return ''.join(html)

    def __repr__(self):
        return "Document %s" % self.fragments
