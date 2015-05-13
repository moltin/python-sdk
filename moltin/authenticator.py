class Authenticator:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def with_client_credentials(self):
        pass

    def with_password(self, username, password):
        pass

    def with_refresh(self, refresh_token):
        pass

