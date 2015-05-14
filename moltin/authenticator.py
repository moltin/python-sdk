from request import Request


class Authenticator:

    uri = "oauth/access_token"

    def __init__(self, client_id, client_secret, request):
        self.request = request
        self.client_id = client_id
        self.client_secret = client_secret
        self.payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

    def auth(self):
        return self.request.auth(self.uri, self.payload)

    def with_client_credentials(self):
        self.payload["grant_type"] = "client_credentials"

        return self.auth()

    def with_password(self, username, password):
        self.payload["grant_type"] = "password"
        self.payload["username"] = username
        self.payload["password"] = password

        return self.auth()

    def with_refresh(self, refresh_token):
        self.payload["grant_type"] = "refresh_token"
        self.payload["refresh_token"] = refresh_token

        return self.auth()

