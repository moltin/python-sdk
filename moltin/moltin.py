from authenticator import Authenticator
from request import Request
from token import TokenContainer

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


class Moltin:

    # Initialise with your client id and secret.
    def __init__(self, client_id, client_secret, version="v1"):
        self.request = Request(version)
        self.authenticator = Authenticator(client_id, client_secret, self.request, TokenContainer())

    def set_api_version(self, version):
        self.request.set_version(version)

    def authenticate(self, username=None, password=None):
        token = self.authenticator.authenticate(username, password)
        # We set the access token for future requests
        self.request.set_access_token(token)

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

    #
