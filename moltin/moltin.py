from authenticator import Authenticator


class AuthError(BaseException):
    pass


class Moltin:

    # Initialise with your client id and secret
    def __init__(self, client_id, client_secret):
        self.authenticator = Authenticator(client_id, client_secret)
        self.auth_result = None

    def authenticate(self, refresh_token=None, username=None, password=None):

        if refresh_token is not None:
            self.auth_result = self.authenticator.with_refresh(refresh_token)
        elif username is not None or password is not None:
            # Make sure we have both user and pass
            if username is None or password is None:
                raise AuthError("Both username and password is required for password authentication")

            self.auth_result = self.authenticator.with_password(username, password)
        else:
            self.auth_result = self.authenticator.with_client_credentials()

