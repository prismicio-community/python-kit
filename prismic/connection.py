# -*- coding: utf-8 -*-

"""
prismic.connection
~~~~~~~~~~~

This module implements the Prismic Connection handlers.

"""

try:  # 2.7
    import urllib.parse as urlparse
except ImportError:  # 3.x
    import urllib as urlparse

import requests
import json
import re
import platform
from collections import OrderedDict
from requests.exceptions import InvalidSchema
from .exceptions import (InvalidTokenError, AuthorizationNeededError,
                         HTTPError, InvalidURLError)
from .cache import ShelveCache
from . import __version__ as prismic_version

def get_using_requests(full_url):
    request = requests.get(full_url, headers={
        "Accept": "application/json",
        "User-Agent": "Prismic-python-kit/%s Python/%s" % (
            prismic_version,
            platform.python_version()
        )
    })
    return request.status_code, request.text, request.headers

def get_json(url, params=None, access_token=None, cache=None, ttl=None, request_handler=None):
    full_params = dict() if params is None else params.copy()
    if cache is None:
        cache = ShelveCache(re.sub(r'/\\', '', url.split('/')[2]))
    if request_handler is None:
        request_handler = get_using_requests
    if access_token is not None:
        full_params["access_token"] = access_token
    full_url = url if len(full_params) == 0 else (url + "?" + urlparse.urlencode(full_params, doseq=1))
    cached = cache.get(full_url)
    if cached is not None:
        return cached
    try:
        status_code, text_result, headers = request_handler(full_url)
        if status_code == 200:
            json_result = json.loads(text_result, object_pairs_hook=OrderedDict)
            expire = ttl or get_max_age(headers)
            if expire is not None:
                cache.set(full_url, json_result, expire)
            return json_result
        elif status_code == 401:
            if len(access_token) == 0:
                raise AuthorizationNeededError()
            else:
                raise InvalidTokenError()
        else:
            raise HTTPError(status_code, str(text_result))
    except InvalidSchema as e:
        raise InvalidURLError(e)


def get_max_age(headers):
    expire_header = headers.get("Cache-Control", None)
    if expire_header is not None:
        m = re.match("max-age=(\d+)", expire_header)
        if m:
            return int(m.group(1))
    return None
