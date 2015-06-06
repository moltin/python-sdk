from . authenticator import Authenticator
from . request import Request
from . token import TokenContainer, TokenFactory
from . endpoints import BaseEndpoint


def create_endpoint_object(name):
    return type(name, (BaseEndpoint, object), {})


class Moltin:
    """
    This class provides an easy way to authenticate, make HTTP requests and do CRUD operations.

    Usage:
    m = Moltin(your_client_id, your_client_secret[, version="v1"])

    To Authenticate with id and secret:
    token = m.authenticate()
    Or with user/pass:
    token, refresh_token = m.authenticate(username="user", password="pass")
    Or with refresh token
    token = m.authenticate(refresh_token=your_refresh_token)

    Once authenticated, the access token is automatically passed to every request
    made through Moltin.
    E.g.
    product = m.get('products/5')
    new_product = m.post('products', params)

    If you need to pass in a previously stored token, use:
    m.set_access_token(your_access_token)
    before making a request

    There's an easier way to interact with most endpoints:
    product = m.Product         # Creates a product wrapper
    product.list()              # lists all products
    product.create(params)      # creates a product, params passed as a dict
    product.find(5)             # finds product with id = 5
    product.find_by(params)     # finds a single product by params passed as a dict,
                                # e.g. {"title": "Banana"}
    product.update(5, params)   # updates product with id = 5 with new params
    product.remove(5)           # removes product with id = 5

    The same wrapper is available with the full list of endpoints given below:
    """

    endpoints = {
        "Brand": "brands",
        "Category": "categories",
        "Collection": "collections",
        "Currency": "currencies",
        "Customer": "customers",
        "Email": "emails",
        "Product": "products",
        "Order": "orders",
        "Shipping": "shipping",
        "Webhooks": "webhooks"
    }

    # Initialise with your client id and secret.
    def __init__(self, client_id, client_secret, version="v1"):
        self.request = Request(version)
        self.authenticator = Authenticator(client_id, client_secret, self.request, TokenContainer())

    def __getattr__(self, name):
        obj_name = name.capitalize()
        if obj_name in self.endpoints:
            endpoint_name = self.endpoints[obj_name]
            endpoint_obj = create_endpoint_object(obj_name)
            return endpoint_obj(self.request, endpoint_name)
        else:
            raise RuntimeError("No such API object: " + name)

    def set_api_version(self, version):
        self.request.set_version(version)

    def set_access_token(self, token_string):
        self.request.set_access_token(TokenFactory.from_string("access", token_string))

    def authenticate(self, username=None, password=None, refresh_token=None):
        refresh = None
        if username and password:
            token, refresh = self.authenticator.authenticate_with_user(username, password)
        elif refresh_token:
            token = self.authenticator.authenticate_with_refresh(refresh_token)
        else:
            token = self.authenticator.authenticate()

        # We set the access token for future requests
        self.request.set_access_token(token)

        if refresh is not None:
            return token, refresh
        else:
            return token

    #
    #  Easy way of interacting with arbitrary API endpoints
    #

    def post(self, uri, payload):
        return self.request.post(uri, payload)

    def get(self, uri):
        return self.request.get(uri)

    def put(self, uri, payload):
        return self.request.put(uri, payload)

    def delete(self, uri):
        return self.request.delete(uri)