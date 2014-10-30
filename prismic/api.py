# -*- coding: utf-8 -*-

"""
prismic.api
~~~~~~~~~~~

This module implements the Prismic API.

"""

import platform
import pkg_resources
from copy import copy, deepcopy
from collections import OrderedDict
from prismic.experiments import Experiments

try:  # 2.7
    import urllib.request as urlrequest
    import urllib.parse as urlparse
    import urllib.error as urlerror
except ImportError:  # 3.x
    import urllib2 as urlrequest
    import urllib as urlparse
    import urllib2 as urlerror
import json
import re

from .exceptions import (InvalidTokenError, AuthorizationNeededError,
                         HTTPError, UnexpectedError, RefMissing)
from .fragments import Fragment, StructuredText
from .cache import ShelveCache
from .utils import string_types
import logging

log = logging.getLogger(__name__)


def get(url, access_token=None, cache=None):
    """Fetches the prismic api JSON.
    Returns :class:`Api <Api>` object.

    :param url: URL to the api of the repository.
    :param access_token: The access token.
    """
    return Api(_get_json(url, access_token=access_token, cache=cache), access_token, cache)


def _get_json(url, params=None, access_token=None, cache=None):
    full_params = dict() if params is None else params.copy()
    if cache is None:
        cache = ShelveCache(re.sub(r'/\\', '', url.split('/')[2]))
    if access_token is not None:
        full_params["access_token"] = access_token
    full_url = url if len(full_params) == 0 else (url + "?" + urlparse.urlencode(full_params, doseq=1))
    cached = cache.get(full_url)
    if cached is not None:
        return cached
    try:
        req = urlrequest.Request(full_url, headers={
            "Accept": "application/json",
            "User-Agent": "Prismic-python-kit/%s Python/%s" % (pkg_resources.require("prismic")[0].version, platform.python_version())
        })
        response = urlrequest.urlopen(req)
        text_result = response.read()
        if not isinstance(text_result, str):
            text_result = text_result.decode('utf-8')
        json_result = json.loads(text_result, object_pairs_hook=OrderedDict)
        expire = _max_age(response)
        if expire is not None:
            cache.set(full_url, json_result, expire)
        return json_result
    except urlerror.HTTPError as http_error:
        if http_error.code == 401:
            if len(access_token) == 0:
                raise AuthorizationNeededError()
            else:
                raise InvalidTokenError()
        else:
            print(full_url)
            raise HTTPError(http_error.code, str(http_error))
    except urlerror.URLError as url_error:
        raise UnexpectedError("Unexpected error: %s" % url_error.reason)


def _max_age(response):
    expire_header = response.info().get("Cache-Control")
    if expire_header is not None:
        m = re.match("max-age=(\d+)", expire_header)
        if m:
            return int(m.group(1))
    return None


class Api(object):
    """
    A Prismic API, pointing to a specific repository. Use prismic.api.get() to fetch one.
    """

    def __init__(self, data, access_token, cache):
        self.cache = cache
        self.refs = [Ref(ref) for ref in data.get("refs")]
        self.bookmarks = data.get("bookmarks")
        self.types = data.get("types")
        self.tags = data.get("tags")
        self.forms = data.get("forms")
        for name in self.forms:
            fields = self.forms[name].get("fields")
            for field in fields:
                if field == "q":
                    fields[field].update({"multiple": True})
        self.experiments = Experiments.parse(data.get("experiments"))
        self.oauth_initiate = data.get("oauth_initiate")
        self.oauth_token = data.get("oauth_token")
        self.access_token = access_token

        self.master = ([ref for ref in self.refs if ref.is_master_ref][:1] or [None])[0]
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
            raise Exception("Bad form name %s, valid form names are: %s" % (name, ', '.join(self.forms)))
        return SearchForm(self.forms.get(name), self.access_token, self.cache)


class Ref(object):

    def __init__(self, data):
        self.id = data.get("id")
        self.ref = data.get("ref")
        self.label = data.get("label")
        self.is_master_ref = data.get("isMasterRef")
        self.scheduled_at = data.get("scheduledAt")


class SearchForm(object):

    """Form to search for documents.

    Most of the methods return self object to allow chaining.
    """

    def __init__(self, form, access_token, cache):
        self.action = form.get("action")
        self.method = form.get("method")
        self.enctype = form.get("enctype")
        self.fields = form.get("fields") or {}
        self.data = {}
        # default values
        for field, value in list(self.fields.items()):
            if value.get("default"):
                self.set(field, value["default"])
        self.access_token = access_token
        self.cache = cache

    def ref(self, ref):
        """:param ref: An :class:`Ref <Ref>` object or an string."""

        if isinstance(ref, Ref):
            ref = ref.ref

        return self.set('ref', ref)

    @staticmethod
    def _serialize(field):
        if isinstance(field, string_types):
            if field.startswith('my.') or field.startswith('document.'):
                return field
            else:
                return '"' + field + '"'
        elif hasattr(field, '__iter__'):
            strings = []
            for item in field:
                strings.append(SearchForm._serialize(item))
            return "[" + ", ".join(strings) + "]"
        else:
            return str(field)

    def query(self, *argv):
        if len(argv) == 0:
            return self
        if isinstance(argv[0], string_types):
            q = argv[0]
        else:
            q = "["
            for predicate in argv:
                op = predicate[0]
                args = []
                for arg in predicate[1:]:
                    args.append(SearchForm._serialize(arg))
                q += "[:d = %(op)s(%(args)s)]" % {
                    'op': op,
                    'args': ", ".join(args)
                }
            q += "]"
        return self.set('q', q)

    def set(self, field, value):
        form_field = self.fields.get(field)
        if form_field and form_field.get("multiple"):
            if not self.data.get(field):
                self.data.update({field: []})
            self.data[field].append(value)
        else:
            self.data.update({field: value})
        return self

    def orderings(self, orderings):
        """Sets the query orderings

        :param String with the orderings predicate
        """
        return self.set("orderings", orderings)

    def submit_assert_preconditions(self):
        if self.data.get('ref') is None:
            raise RefMissing()

    def submit(self):
        self.submit_assert_preconditions()
        return Response(_get_json(self.action, self.data, self.access_token, self.cache))

    def page(self, page_number):
        """Set query page number

        :param page_number: int representing the page number
        """
        return self.set("page", page_number)

    def page_size(self, nb_results):
        """Set query page size

        :param nb_results: int representing the number of results per page
        """
        return self.set("pageSize", nb_results)

    def pageSize(self, nb_results):
        """Deprecated: use page_size instead
        """
        return self.page_size(nb_results)

    def count(self):
        """Count the total number of results
        """
        return copy(self).pageSize(1).submit().total_results_size

    def __copy__(self):
        cp = type(self)({}, self.access_token, self.cache)
        cp.action = deepcopy(self.action)
        cp.method = deepcopy(self.method)
        cp.enctype = deepcopy(self.enctype)
        cp.fields = deepcopy(self.fields)
        cp.data = deepcopy(self.data)
        return cp


class Response(object):
    """
    Prismic's response to a query.

    Attributes:
        documents (:class:`prismic.api.Document <prismic.api.Document>`): the resulting documents
        page (int): the page in this result, starting by 1
        results_per_page (int): max result in a page
        total_results_size: total number of results for this query
        total_pages (int): total number of pages for this query
        next_page (str): ref of the next page (may be None)
        prev_page (str): ref of the previous page (may be None)
        results_size (int) : number of results actually returned for the current page
    """

    def __init__(self, data):
        self._data = data
        self.documents = [Document(d) for d in data.get("results")]
        self.page = data.get("page")
        self.next_page = data.get("next_page")
        self.prev_page = data.get("prev_page")
        self.results_per_page = data.get("results_per_page")
        self.total_pages = data.get("total_pages")
        self.total_results_size = data.get("total_results_size")
        self.results_size = data.get("results_size")

    def __getattr__(self, name):
        return self._data.get(name)

    def __repr__(self):
        return "Response %s" % self._data


class LinkedDocument(object):

    def __init__(self, data):
        self._data = data

    def get_id(self):
        return self._data.get("id")

    def get_slug(self):
        return self._data.get("slug")

    def get_typ(self):
        return self._data.get("typ")

    def get_tags(self):
        return self._data.get("tags")


class Document(Fragment.WithFragments):

    def __init__(self, data):
        Fragment.WithFragments.__init__(self, {})
        self._data = data
        self.linked_documents = []

        fragments = data.get("data").get(self.type) if "data" in data else {}
        for (fragment_name, fragment_value) in list(fragments.items()):
            f_key = "%s.%s" % (self.type, fragment_name)

            if isinstance(fragment_value, list):
                for index, fragment_value_element in enumerate(fragment_value):
                    self.fragments["%s[%s]" % (f_key, index)] = Fragment.from_json(
                        fragment_value_element)

            elif isinstance(fragment_value, dict):
                self.fragments[f_key] = Fragment.from_json(fragment_value)

        if "linked_documents" in data:
            self.linked_documents = [LinkedDocument(d) for d in data.get("linked_documents")]

    def __getattr__(self, name):
        return self._data.get(name)

    @property
    def slug(self):
        return self.slugs[0] if self.slugs else "-"

    def __repr__(self):
        return "Document %s" % self.fragments
