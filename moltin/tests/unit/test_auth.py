from moltin.moltin import Moltin
from moltin.exception import *
from moltin.request import Request
from moltin.token import *
from moltin.authenticator import Authenticator
from . mock_response import mock_auth_response
from sure import expect

import mock

m = Authenticator("", "", Request("v1"), TokenContainer())


@mock.patch("moltin.requests.post")
def test_client_credentials(mock_post):
    mock_post.return_value = mock_auth_response()
    token = m.authenticate()
    expect(len(token.token) > 0).to.eql(True)


@mock.patch("moltin.requests.post")
def test_incorrect_client_credentials(mock_post):
    mock_post.return_value = mock_auth_response({"error": "Incorrect deets"})
    m = Moltin(client_id="asd",
               client_secret="def")
    m.authenticate.should.throw(RequestError)

@mock.patch("moltin.requests.post")
def test_user_and_pass_incorrect(mock_post):
    mock_post.return_value = mock_auth_response({"error": "Incorrect deets"})
    m.authenticate_with_user.when.called_with(username="test", password="test").should.throw(RequestError)


@mock.patch("moltin.requests.post")
def test_user_and_pass_correct(mock_post):
    mock_post.return_value = mock_auth_response({"access_token": "somestring", "token_type": "Bearer", "refresh_token": "someotherstring"})
    token, refresh = m.authenticate_with_user(username="correct_username", password="correct_password")
    expect(len(refresh.token) > 0).to.eql(True)