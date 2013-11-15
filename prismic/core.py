
import urllib
import urllib2
import json
import logging

log = logging.getLogger(__name__)


class GenericWSRequest(object):
    """Make HTTP requests to get the JSON."""

    def __init__(self, url):
        self.url = url
        self.get_params = None
        self.headers = None
        self.response = None
        self.response_contents = None

    def set_get_params(self, params):
        encoded_params = urllib.urlencode(params, doseq=True)
        if self.get_params is None:
            self.get_params = encoded_params
        else:
            self.get_params = self.get_params + "&" + encoded_params

    def set_access_token(self, access_token):
        values = {
            "access_token": access_token
        }
        self.set_get_params(values)

    def set_headers(self, headers):
        self.headers = headers

    def accept_json(self):
        headers = {
            "Accept": "application/json"
        }
        self.set_headers(headers)

    def get_url(self):
        if self.get_params is None:
            return self.url
        else:
            return self.url + "?" + self.get_params

    def get(self):
        log.info("Get the url " + self.get_url())
        log.debug("Headers " + str(self.headers))
        req = urllib2.Request(self.get_url(), headers=self.headers)
        response = urllib2.urlopen(req)

        self.response = response
        self.response_contents = response.read()

    def get_json(self):
        self.accept_json()
        self.get()
        log.debug("Api json: " + self.response_contents)
        return json.loads(self.response_contents)
