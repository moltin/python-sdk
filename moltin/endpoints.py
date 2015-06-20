from . url import sanitize_url_fragment
from . exception import *


class BaseEndpoint(object):

    def __init__(self, request, endpoint):
        self.request = request
        self.endpoint = sanitize_url_fragment(endpoint)

    def _url_with(self, *params):
        def add_to_endpoint(endpoint, param):
            return endpoint + "/" + str(param)

        return reduce(add_to_endpoint, params, self.endpoint)


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

    def __init__(self, request, endpoint, cart_id):
        super(CartEndpoint, self).__init__(request, endpoint)
        self.id = cart_id

    def add_item(self, params):
        self.request.post(self._url_with(self.id), params)

    def add_variation(self, params):
        self.add_item(params)

    def update_item(self):
        pass

    def contents(self):
        pass

    def list(self):
        pass

    def has_item(self):
        pass

    def get_item(self, item_id):
        pass

    def delete_item(self, item_id):
        pass

    def checkout_options(self):
        pass

    def checkout(self):
        pass

