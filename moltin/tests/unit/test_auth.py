import moltin
from moltin.moltin import Moltin
from moltin.exception import *
from moltin.request import Request
from moltin.token import *
from moltin.authenticator import Authenticator
from time import time
from sure import expect

import mock

m = Authenticator("", "", Request("v1"), TokenContainer())


def create_mock_response(hash_to_return=None):
    hash_to_return = hash_to_return or {"access_token": "somestring"}
    hash_to_return["expires_in"] = 3600
    hash_to_return["expires"] = time() + hash_to_return["expires_in"]

    mock_response = mock.Mock(moltin.requests.Response)
    mock_response.json.return_value = hash_to_return
    return mock_response


@mock.patch("moltin.requests.post")
def test_client_credentials(mock_post):
    mock_post.return_value = create_mock_response()
    token = m.authenticate()
    expect(len(token.token) > 0).to.eql(True)


@mock.patch("moltin.requests.post")
def test_incorrect_client_credentials(mock_post):
    mock_post.return_value = create_mock_response({"error": "Incorrect deets"})
    m = Moltin(client_id="asd",
               client_secret="def")
    m.authenticate.should.throw(RequestError)


@mock.patch("moltin.requests.post")
def test_user_but_no_pass(mock_post):
    mock_post.return_value = None
    m.authenticate.when.called_with(username="test").should.throw(FieldTypeError)


@mock.patch("moltin.requests.post")
def test_pass_but_no_user(mock_post):
    mock_post.return_value = None
    m.authenticate.when.called_with(password="test").should.throw(FieldTypeError)


@mock.patch("moltin.requests.post")
def test_user_and_pass_incorrect(mock_post):
    mock_post.return_value = create_mock_response({"error": "Incorrect deets"})
    m.authenticate.when.called_with(username="test", password="test").should.throw(RequestError)


@mock.patch("moltin.requests.post")
def test_user_and_pass_correct(mock_post):
    mock_post.return_value = create_mock_response({"access_token": "somestring", "refresh_token": "someotherstring"})
    m.authenticate(username="correct_username", password="correct_password")
    expect(len(m.tokens.get("refresh").token) > 0).to.eql(True)