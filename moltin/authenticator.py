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

    def with_client_credentials(self):
        self.payload["grant_type"] = "client_credentials"

        return self.request.auth(self.uri, self.payload)

    def with_password(self, username, password):
        pass

    def with_refresh(self, refresh_token):
        pass

