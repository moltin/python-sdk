from authenticator import Authenticator
from exception import *
from request import Request


class Moltin:

    # Initialise with your client id and secret
    def __init__(self, client_id, client_secret, version="v1"):
        self.request = Request(version)
        self.authenticator = Authenticator(client_id, client_secret, self.request)
        self.auth_result = None
        self.access_token = None

    def authenticate(self, refresh_token=None, username=None, password=None):

        if refresh_token is not None:
            self.auth_result = self.authenticator.with_refresh(refresh_token)
        elif username is not None or password is not None:
            # Make sure we have both user and pass
            if username is None or password is None:
                raise RequestError("Both username and password is required for password authentication")

            self.auth_result = self.authenticator.with_password(username, password)
        else:
            self.auth_result = self.authenticator.with_client_credentials()

        self.access_token = self.auth_result['access_token']
        return self.access_token

