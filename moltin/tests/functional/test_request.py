from moltin.request import Request
from moltin.token import TokenMaker
from moltin.exception import *
import sure
from sure import expect
from time import time

r = Request("v1")


def set_access_token(token, expires):
    params = {
        "access_token": token,
        "expires": expires,
        "expires_in": 3600
    }

    r.set_access_token(TokenMaker.from_response("access", params))


def test_access_token_set():
    expect(r.headers["Authorization"]).to.eql("Bearer somestring")


def test_request_with_invalid_code():
    set_access_token("somestring", time())

    r.get.when.called_with('products/').should.throw(RequestError)