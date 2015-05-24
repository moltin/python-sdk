import time
from exception import *


class TokenContainer:

    tokens = {}

    def __init__(self, access_token=None, refresh_token=None):
        self.tokens["access"] = access_token
        self.tokens["refresh"] = refresh_token

    def set(self, token_type, token):
        self.tokens[token_type] = token

    def get(self, token_type):
        return self.tokens[token_type]


class Token:
    def __init__(self, token, type):
        self.token = token
        self.type = type

    def has_expired(self):
        return False


class RefreshToken(Token):
    pass


class AccessToken(Token):
    def __init__(self, token, type, expires, expires_in):
        Token.__init__(self, token, type)
        self.expires = expires
        self.expires_in = expires_in

    def has_expired(self):
        return self.expires < time.time() - 5


class TokenMaker:
    def __init__(self):
        pass

    @staticmethod
    def from_response(token_type, response):
        token_key = token_type.lower() + "_token"

        if token_type == "refresh":
            token = RefreshToken(response[token_key], response["token_type"])
        elif token_type == "access":
            token = AccessToken(response[token_key], response["token_type"], response["expires"], response["expires_in"])
        else:
            raise FieldTypeError("No such token: " + token_type)

        return token