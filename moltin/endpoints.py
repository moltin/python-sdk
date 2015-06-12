from . url import sanitize_url_fragment
from . exception import *


class BaseEndpoint(object):

    def __init__(self, request, endpoint):
        self.request = request
        self.endpoint = sanitize_url_fragment(endpoint)

    def _url_with(self, param):
        return self.endpoint + "/" + str(param)


class Endpoint(BaseEndpoint):

    def find(self, id):
        return self.find_by({"id": id})

    def update(self, id, params):
        return self.request.put(self._url_with(id), payload=params)

    def remove(self, id):
        return self.request.delete(self._url_with(id))

    def list(self):
        return self.request.get(self.endpoint)

    def find_by(self, params):
        try:
            return self.request.get(self.endpoint, payload=params)
        except RequestError:  # If we can't find the resource
            return None

    def create(self, params):
        return self.request.post(self.endpoint, payload=params)

class CartEndpoint(BaseEndpoint):

    def addItem(self):
        pass

    def addVariation(self):
        pass

    def updateItem(self):
        pass

    def list(self):
        pass

    def hasItem(self):
        pass

class Cart:
