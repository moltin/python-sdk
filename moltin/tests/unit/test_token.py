import time
from moltin.token import *
from sure import expect


def test_refresh_token_maker():
    response = {"refresh_token": "somestring"}
    token = TokenMaker.from_response("refresh", response)
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(False)


def test_access_token_maker():
    response = {"access_token": "somestring", "expires": time.time() - 3600, "expires_in": 0}
    token = TokenMaker.from_response("access", response)
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(True)


def test_not_expired():
    token = AccessToken("somestring", time.time() + 3600, 3600)
    expect(token.has_expired()).to.eql(False)


def test_expired():
    token = AccessToken("somestring", time.time() - 10, 3600)
    expect(token.has_expired()).to.eql(True)