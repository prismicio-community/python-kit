
import urllib
import urllib2
import json

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

    def get_json(self):
        self.accept_json()
        self.get()
        # print self.response_contents
        return json.loads(self.response_contents)
