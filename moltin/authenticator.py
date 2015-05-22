from token import TokenMaker
from exception import *


class Authenticator:

    uri = "oauth/access_token"

    def __init__(self, client_id, client_secret, request, token_container):
        self.request = request
        self.client_id = client_id
        self.client_secret = client_secret
        self.payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        self.tokens = token_container

    def authenticate(self, username=None, password=None):
        if self.tokens.get("refresh") is not None:
            self.with_refresh()

        elif username is not None or password is not None:
            self.with_password(username, password)

        else:
            self.with_client_credentials()
        return self.tokens.get("access")

    def make_request(self):
        response = self.request.auth(self.uri, self.payload)
        self.tokens.set("access", TokenMaker.from_response("access", response))
        return response

    def with_client_credentials(self):
        self.payload["grant_type"] = "client_credentials"

        return self.make_request()

    def with_password(self, username, password):
        if username is None or password is None:
            raise FieldTypeError(
                "Both username and password is required for user/pass authentication"
            )

        self.payload["grant_type"] = "password"
        self.payload["username"] = username
        self.payload["password"] = password

        response = self.make_request()
        self.tokens.set("refresh", TokenMaker.from_response("refresh", response))
        return response

    def with_refresh(self):
        self.payload["grant_type"] = "refresh_token"
        self.payload["refresh_token"] = self.tokens.get("refresh")

        return self.make_request()