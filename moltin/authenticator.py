from . token import TokenFactory


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

    def authenticate(self):
        self.with_client_credentials()
        return self.tokens.get("access")

    def authenticate_with_user(self, username, password):
        self.with_user(username, password)
        return self.tokens.get("access"), self.tokens.get("refresh")

    def authenticate_with_refresh(self, refresh_token):
        self.tokens.set("refresh", TokenFactory.from_string("refresh", refresh_token))
        self.with_refresh()
        return self.tokens.get("access")

    def make_request(self):
        response = self.request.auth(self.uri, self.payload)
        self.tokens.set("access", TokenFactory.from_response("access", response))
        return response

    def with_client_credentials(self):
        self.payload["grant_type"] = "client_credentials"

        return self.make_request()

    def with_user(self, username, password):
        self.payload["grant_type"] = "password"
        self.payload["username"] = username
        self.payload["password"] = password

        response = self.make_request()
        self.tokens.set("refresh", TokenFactory.from_response("refresh", response))
        return response

    def with_refresh(self):
        self.payload["grant_type"] = "refresh_token"
        self.payload["refresh_token"] = self.tokens.get("refresh").token

        return self.make_request()