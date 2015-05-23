import moltin
import mock
from time import time

def create_mock_response(hash_to_return=None):
    hash_to_return = hash_to_return or {"access_token": "somestring"}
    hash_to_return["expires_in"] = 3600
    hash_to_return["expires"] = time() + hash_to_return["expires_in"]

    mock_response = mock.Mock(moltin.requests.Response)
    mock_response.json.return_value = hash_to_return
    return mock_response