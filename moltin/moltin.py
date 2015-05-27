from authenticator import Authenticator
from request import Request
from token import TokenContainer
from endpoints import BaseEndpoint
import types

# The Moltin Python SDK
#
# This class should be your entrance point to the Moltin Python SDK
#
# Initialisation
#
# Initialise Moltin with your client_id and client_secret
# If you require a specific API version, pass it in as the version kwarg
#
# Authentication
#
# Once initialised, call authenticate()
# The authenticate() method always returns your access_token, but the token is also
# automatically used for all future requests on the Moltin object
#
# By default, authentication will be done using the client_id and secret
# To change authentication type:
# For user/pass authentication, pass in username & password as kwargs
# For refresh token authentication, pass the refresh_token in as the refresh_token kwarg
#
# Once you authenticate using user/pass, the refresh token is available
# from Moltin.refresh_token


def create_endpoint_object(name):
    return type(name, (BaseEndpoint, object), {})


class Moltin:
    """
    This class provides an easy way to authenticate, make HTTP requests and do CRUD operations.

    Usage:
    m = Moltin(your_client_id, your_client_secret[, version="v1"])

    To Authenticate:
    m.authenticate()
    Or with user/pass
    m.authenticate(username="user", password="pass")

    Once authenticated, the access token is automatically passed to every request
    made through Moltin.
    E.g.
    product = m.get('products/5')
    new_product = m.post('products', params)

    There's an easier way to interact with most endpoints:
    product = m.Product         # Creates a product wrapper
    product.list()              # lists all products
    product.create(params)      # creates a product, parameters passed as a dict
    product.find(5)             # finds product by id = 5
    product.find_by(params)     # finds a single product by params passed as a dict, e.g. {"title": "Banana"}
    product.update(5, params)   # updates product with id = 5 with new params
    product.remove(5)           # removes product with id = 5

    The same wrapper is available with the full list of endpoints given below:
    """

    endpoints = {
        "Address": "addresses",
        "Brand": "brands",
        "Cart": "cart",
        "Category": "categories",
        "Checkout": "checkout",
        "Collection": "collections",
        "Currency": "currencies",
        "Customer": "customers",
        "CustomerGroup": "customer_groups",
        "Email": "emails",
        "Entry": "entries",
        "Field": "fields",
        "File": "files",
        "Flow": "flow",
        "Gateway": "gateways",
        "Language": "languages",
        "Modifier": "modifiers",
        "Product": "products",
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

    def authenticate(self, username=None, password=None):
        token = self.authenticator.authenticate(username, password)
        # We set the access token for future requests
        self.request.set_access_token(token)
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