import moltin
import mock
from time import time

hashes = {
    "default": {"status": True, "result": {}},
    "default_auth": {
        "access_token": "somestring",
        "refresh_token": "somestring",
        "token_type": "Bearer",
        "expires_in": 3600,
        "expires": time() + 3600
    }
}


def mock_auth_response(modified_params=None):
    hash = hashes["default_auth"].copy()
    if modified_params:
        hash.update(modified_params)

    return mock_response(hash)


def mock_response(hash_to_return=None, result=None):
    hash_to_return = hash_to_return or hashes['default']
    if result:
        hash_to_return["result"] = result
    response = mock.Mock(moltin.requests.Response)
    response.json.return_value = hash_to_return

    return response