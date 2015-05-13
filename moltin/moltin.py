from authenticator import Authenticator


class AuthError(BaseException):
    pass


class Moltin:

    # Initialise with your client id and secret
    def __init__(self, client_id, client_secret):
        self.authenticator = Authenticator(client_id, client_secret)
        self.auth_result = None


