import moltin
from moltin.moltin import Moltin
from sure import expect
from moltin.exception import *
from moltin.tests.credentials import *
import mock

m = Moltin(CLIENT_ID, CLIENT_SECRET)


def create_mock_response(hash_to_return=None):
    if hash_to_return is None:
         hash_to_return = {"access_token": "somestring"}

    mock_response = mock.Mock(moltin.requests.Response)
    mock_response.json.return_value = hash_to_return
    return mock_response


@mock.patch("moltin.requests.post")
def test_client_credentials(mock_post):
    mock_post.return_value = create_mock_response()
    token = m.authenticate()
    expect(len(token) > 0).to.eql(True)


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
    m.authenticate(username=USERNAME, password=PASSWORD)
    expect(len(m.refresh_token) > 0).to.eql(True)


@mock.patch("moltin.requests.post")
def test_auth_with_incorrect_refresh(mock_post):
    mock_post.return_value = create_mock_response({"error": "Bad request token"})
    m.authenticate.when.called_with(refresh_token="test").should.throw(RequestError)


@mock.patch("moltin.requests.post")
def test_auth_with_correct_refresh(mock_post):
    mock_post.return_value = create_mock_response()
    m.authenticate(refresh_token=m.refresh_token)
    expect(len(m.access_token) > 0).to.eql(True)