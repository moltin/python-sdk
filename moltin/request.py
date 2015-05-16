import requests
from exception import *


class Request:

    def __init__(self, version):
        self.base = "https://api.molt.in/"
        self.version = version + "/"  # api version with trailing slash for URI composition
        self.auth_token = None

    def set_version(self, version):
        self.version = version

    def get(self, url):
        pass

    def post(self, trailing_uri, payload, omit_version=False):

        if omit_version:
            request_url = self.base + trailing_uri
        else:
            request_url = self.base + self.version + trailing_uri

        r = requests.post(request_url, data=payload)
        response = r.json()

        if 'error' in response:
            raise RequestError(response['error'])
        else:
            return response

    def auth(self, auth_uri, payload):
        return self.post(auth_uri, payload, omit_version=True)

    def put(self, url, payload):
        pass

    def delete(self, url):
        pass