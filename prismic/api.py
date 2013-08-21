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


def get(url, access_token):
    try:
        values = {
            "access_token": access_token
        }

        request = GenericWSRequest(url)
        request.set_get_params(values)
        return Api(request.get_json(), access_token)

    except urllib2.HTTPError as http_error:
        if http_error.code == 401:
            raise AuthorizationNeededError() if (len(access_token) == 0) else InvalidTokenError()
        else:
            raise HTTPError(http_error.code, http_error.reason)

    except urllib2.URLError as url_error:
        raise UnexpectedError("Unexpected error: %s" % url_error.reason)

class Api(object):

    def __init__(self, data, access_token):
        self.refs = data.get("refs")
        self.bookmarks = data.get("bookmarks")
        self.types = data.get("types")
        self.tags = data.get("tags")
        self.forms = data.get("forms")
        self.oauth_initiate = data.get("oauth_initiate")
        self.oauth_token = data.get("oauth_token")

        self.access_token = access_token

    def ref(self, label):
        ref = [ref for ref in self.refs if ref.get("label") == label]
        return Ref(ref[0]) if ref else None

    def form(self, name):
        return SearchForm(self, self.forms.get(name))


class Ref(object):
    def __init__(self, data):
        self.ref = data.get("ref")
        self.label = data.get("label")
        self.isMasterRef = data.get("scheduledAt")


class SearchForm(object):
    def __init__(self, api, form):
        self.api = api

        self.action = form.get("action")
        self.method = form.get("method")
        self.enctype = form.get("enctype")
        self.fields = form.get("fields")
        self.fields_data = {}

    def ref(self, label=None, ref_id=None):
        if label:
            ref = self.api.ref(label)
            if ref:
                self.fields_data.update({'ref': ref.ref})
                return True
            else:
                return False
        elif ref_id:
            self.fields_data.update({'ref': ref_id})
            return True
        return False

    def query(self, query):
        self.fields_data.update({'q': query})

    def submit_preconditions(self):
        if (self.fields_data.get('ref') == None):
            raise RefMissing

    def submit(self):
        self.submit_preconditions()
        request = GenericWSRequest(self.action)
        request.set_get_params(self.fields_data)
        return [Document(doc) for doc in request.get_json()]


class Document(object):

    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")
        self.href = data.get("href")
        self.tags = data.get("tags")
        self.slugs = data.get("slugs")
        self.fragments = data.get("fragments")

    @property
    def slug(self):
        return self.slugs[0] if self.slugs else "-"