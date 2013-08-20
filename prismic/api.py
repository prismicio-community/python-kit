# -*- coding: utf-8 -*-

"""
prismic.api
~~~~~~~~~~~

This module implements the Prismic API.

"""

import urllib
import urllib2
import json
from .exceptions import (InvalidTokenError,
                         AuthorizationNeededError, HTTPError, UnexpectedError)


class GenericWSRequest(object):
    def __init__(self, url):
        self.url = url
        self.get_params = None
        self.headers = None
        self.response = None
        self.response_contents = None

    def set_get_params(self, params):
        self.get_params = urllib.urlencode(params)

    def set_headers(self, headers):
        self.headers = headers

    def accept_json(self):
        headers = {
            "Accept": "application/json"
        }
        self.set_headers(headers)

    def get_url(self):
        if self.get_params == None:
            return self.url
        else:
            return self.url + "?" + self.get_params

    def get(self):
        print("Get the url " + self.get_url())
        req = urllib2.Request(self.get_url(), headers=self.headers)
        response = urllib2.urlopen(req)

        self.response = response
        self.response_contents = response.read()

    def get_as_json(self):
        self.accept_json()
        self.get()
        return json.loads(self.response_contents)

def get(url, access_token):
    try:
        values = {
            "access_token": access_token
        }

        request = GenericWSRequest(url)
        request.set_get_params(values)
        return Api(request.get_as_json(), access_token)

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

    def get_ref_by_label(self, ref_label):
        ref = [ref for ref in self.refs if ref.get("label") == ref_label]
        return ref[0] if ref else None


    def get_form(self, name):
        return SearchForm(self, self.forms.get(name))


class SearchForm(object):
    def __init__(self, api, form):
        self.api = api

        self.action = form.get("action")
        self.method = form.get("method")
        self.enctype = form.get("enctype")
        self.fields = form.get("fields")
        self.fields_data = {}

    def ref(self, ref):
        self.fields_data.update({'ref': ref})

    def ref_by_label(self, ref_label):
        ref = self.api.get_ref_by_label(ref_label)
        if ref:
            self.fields_data.update({'ref': ref.get("id")})
            return True
        else:
            return False

    def query(self, query):
        self.fields_data.update({'query': query})

    def submit(self):
        request = GenericWSRequest(self.action)
        request.set_get_params(self.fields_data)
        print request.get_as_json()

