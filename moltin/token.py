import time


class TokenContainer:

    tokens = {}

    def __init__(self, access_token=None, refresh_token=None):
        self.tokens["access"] = access_token
        self.tokens["refresh"] = refresh_token

    def set(self, access_or_refresh, token):
        self.tokens[access_or_refresh] = token

    def get(self, access_or_refresh):
        return self.tokens[access_or_refresh]

    def token_exists(self, access_or_refresh):
        return access_or_refresh in self.tokens


class Token:
    def __init__(self, access_or_refresh, params):
        self.token = params[access_or_refresh + "_token"]
        self.type = params["token_type"]

    def has_expired(self):
        return False


class RefreshToken(Token):
    def __init__(self, params):
        Token.__init__(self, "refresh", params)


class AccessToken(Token):
    def __init__(self, params):
        Token.__init__(self, "access", params)
        self.expires = params["expires"]
        self.expires_in = params["expires_in"]

    def has_expired(self):
        return self.expires < time.time() - 5


class TokenFactory:

    tokens = {"refresh": RefreshToken, "access": AccessToken}

    @staticmethod
    def from_string(token_type, string):
        token_key = TokenFactory.key_from_type(token_type)
        token = TokenFactory.tokens[token_type](
            {
                token_key: string,
                "token_type": "Bearer",
                "expires": time.time(),
                "expires_in": 3600
            })

        return token

    @staticmethod
    def key_from_type(token_type):
        token_key = token_type.lower() + "_token"
        return token_key

    @staticmethod
    def from_response(token_type, response):
        return TokenFactory.tokens[token_type](response)