from authenticator import Authenticator
from exception import *
from request import Request


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
        self.authenticator = Authenticator(client_id, client_secret, self.request)
        self.auth_result = None
        self.access_token = None
        self.refresh_token = None

    def authenticate(self, refresh_token=None, username=None, password=None):
        if refresh_token is not None:
            self.auth_result = self.authenticator.with_refresh(refresh_token)

        elif username is not None or password is not None:
            # Make sure we have both user and pass
            if username is None or password is None:
                raise FieldTypeError(
                    "Both username and password is required for user/pass authentication"
                )

            self.auth_result = self.authenticator.with_password(username, password)
            self.refresh_token = self.auth_result["refresh_token"]

        else:
            self.auth_result = self.authenticator.with_client_credentials()

        self.access_token = self.auth_result['access_token']
        return self.access_token

