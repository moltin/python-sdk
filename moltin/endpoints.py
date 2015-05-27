from url import sanitize_url_fragment
from exception import *


class BaseEndpoint():
    # This class is a wrapper around the moltin.request module
    # By subclassing it with a particular endpoint, it provides a more abstracted way to
    # do CRUD operations on that endpoint.
    # E.g.
    #
    # class Product(BaseEndpoint):
    #   def __init__(request):
    #        BaseEndpoint.__init__(request, "product")
    #
    # Usage:
    # product = Product()
    # product.create(params)
    # product.find(5) ## finds by id
    # product.find_by(params) ## finds product that matches given params

    def __init__(self, request, endpoint):
        self.request = request
        self.endpoint = sanitize_url_fragment(endpoint)

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

    def _url_with(self, param):
        return self.endpoint + "/" + str(param)