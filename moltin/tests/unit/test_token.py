from . mock_response import mock_auth_response
from moltin.token import *
from sure import expect


def test_refresh_token_maker():
    response = mock_auth_response()
    token = TokenFactory.from_response("refresh", response.json())
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(False)


def test_access_token_maker():
    response = mock_auth_response({"expires": (time.time() - 10)})
    token = TokenFactory.from_response("access", response.json())
    expect(token.token).to.eql("somestring")
    expect(token.has_expired()).to.eql(True)