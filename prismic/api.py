# -*- coding: utf-8 -*-

"""
prismic.api
~~~~~~~~~~~

This module implements the Prismic API.

"""

import urllib
import urllib2
from .exceptions import (InvalidTokenError,
                         AuthorizationNeededError, HTTPError, UnexpectedError)
import json


def get(url, access_token):
    try:
        values = {
            "access_token": access_token
        }
        headers = {
            "Accept": "application/json"
        }
        url_values = urllib.urlencode(values)
        full_url = url + "?" + url_values

        # print "full_url",full_url

        req = urllib2.Request(full_url, headers=headers)
        response = urllib2.urlopen(req)
        contents = response.read()
        # print "read",contents

        json_response = json.loads(contents)

        return Api(json_response)

    except urllib2.HTTPError as http_error:
        if http_error.code == 401:
            if len(access_token) == 0:
                raise AuthorizationNeededError()
            else:
                raise InvalidTokenError()
        else:
            raise HTTPError(http_error.code, http_error.reason)

    except urllib2.URLError as url_error:
        raise UnexpectedError("Unexpected error: %s" % url_error.reason)


class Api(object):

    def __init__(self, data):
        self.data = data

    def refs(self):
        return self.data.get("refs")

    def bookmarks(self):
        return self.data.get("bookmarks")

    def forms(self):
        return self.data.get("forms")
