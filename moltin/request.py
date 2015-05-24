import requests
from url import sanitize_url_fragment
from exception import *


def with_error_handling(callback, *args, **kwargs):
    response = callback(*args, **kwargs)
    r = response.json()

    if 'error' in r:
        raise RequestError(r['error'])
    elif 'result' in r:
        result = r['result']
    elif 'message' in r:
        result = r['message']
    else:
        result = r

    return result


class Request:

    def __init__(self, version):
        self.base = "https://api.molt.in/"
        self.version = None
        self.access_token = None
        self.headers = {}
        self.set_version(version)  # api version with trailing slash for URI composition

    def set_version(self, version):
        self.version = sanitize_url_fragment(version) + "/"

    def set_access_token(self, token):
        self.access_token = token
        self.set_auth_header(token)

    def set_auth_header(self, token):
        self.headers["Authorization"] = "Bearer " + token.token

    def get(self, url, params=None):
        if params is None:
            params = {}
        return with_error_handling(requests.get, self.make_url(url), headers=self.headers, params=params)

    def post(self, trailing_uri, payload, auth=False):
        if auth:
            headers = {}
            request_url = self.make_auth_url(trailing_uri)
        else:
            headers = self.headers
            request_url = self.make_url(trailing_uri)

        return with_error_handling(requests.post, request_url, data=payload, headers=headers)

    def auth(self, auth_uri, payload):
        return self.post(auth_uri, payload, auth=True)

    def put(self, url, payload):
        pass

    def delete(self, url):
        pass

    def make_auth_url(self, trailing_uri):
        return self.base + trailing_uri

    def make_url(self, trailing_uri):
        return self.base + self.version + sanitize_url_fragment(trailing_uri)