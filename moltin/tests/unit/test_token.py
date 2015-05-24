import time
from mock_response import mock_auth_response
from moltin.token import *
from sure import expect


def test_refresh_token_maker():
    response = mock_auth_response()
    token = TokenMaker.from_response("refresh", response.json())
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(False)


def test_access_token_maker():
    response = mock_auth_response({"expires": (time.time() - 10)})
    token = TokenMaker.from_response("access", response.json())
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(True)


def test_not_expired():
    token = AccessToken("somestring", "Bearer", time.time() + 3600, 3600)
    expect(token.has_expired()).to.eql(False)


def test_expired():
    token = AccessToken("somestring", "Bearer", time.time() - 10, 3600)
    expect(token.has_expired()).to.eql(True)