from moltin.request import Request
from moltin.token import TokenFactory
from moltin.exception import *
import sure
import mock
from . mock_response import mock_auth_response
from sure import expect
from time import time

r = Request("v1")


def set_access_token(token, expires):
    params = {
        "access_token": token,
        "token_type": "Bearer",
        "expires": expires,
        "expires_in": 3600
    }

    r.set_access_token(TokenFactory.from_response("access", params))


def test_access_token_set():
    set_access_token("somestring", time() + 3600)
    expect(r.headers["Authorization"]).to.eql("Bearer somestring")


@mock.patch("moltin.requests.get")
def test_request_with_invalid_code(mock_get):
    mock_get.return_value = mock_auth_response({"error": "Invalid Auth Code"})
    set_access_token("somestring", time() + 3600)
    r.get.when.called_with('products/').should.throw(RequestError)


@mock.patch("moltin.requests.get")
def test_request_with_invalid_code(mock_get):
    mock_get.return_value = mock_auth_response({"result": {"products": []}})
    response = r.get('products/')
    expect(response["products"]).to.eql([])