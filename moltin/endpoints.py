import uuid

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

    def __init__(self, request, endpoint, cart_id=None):
        super(CartEndpoint, self).__init__(request, endpoint)
        self.id = cart_id or uuid.uuid4()
        self.endpoint = self._url_with(cart_id)

    def add_item(self, params):
        return self.request.post(self.endpoint, params)

    def add_variation(self, params):
        return self.add_item(params)

    def update_item(self, item_id, params):
        return self.request.put(
            self._url_with(self.id, "items", item_id),
            params
        )

    def contents(self):
        return self.request.get(self.endpoint)

    def has_item(self, item_id):
        return bool(self.request.get(self._url_with("has", item_id))["status"])

    def get_item(self, item_id):
        return self.request.get(self._url_with("item", item_id))

    def delete_item(self, item_id):
        return self.request.delete(self._url_with("item", item_id))

    def checkout_options(self):
        return self.request.get(self._url_with("checkout"))

    def checkout(self, params):
        return self.request.post(self._url_with("checkout"), params)

    def delete(self):
        return self.request.delete(self.endpoint)


class CheckoutEndpoint(BaseEndpoint):

    def payment(self, method, order_id, params):
        return self.request.post(self._url_with("payment", method, order_id), params)
