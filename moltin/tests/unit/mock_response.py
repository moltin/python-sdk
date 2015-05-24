import moltin
import mock
from time import time

hashes = {
    "default": {"status": True, "result": {}},
    "default_auth": {"access_token": "somestring"}
}


def mock_auth_response(hash_to_return=None):
    hash_to_return = hash_to_return or hashes['default_auth']
    hash_to_return["expires_in"] = 3600
    hash_to_return["expires"] = time() + hash_to_return["expires_in"]

    return mock_response(hash_to_return)


def mock_response(hash_to_return=None, result=None):
    hash_to_return = hash_to_return or hashes['default']
    if result:
        hash_to_return["result"] = result

    response = mock.Mock(moltin.requests.Response)
    response.json.return_value = hash_to_return

    return response