from moltin.moltin import Moltin
from sure import expect
from moltin.exception import *
import json
import os

# To run these API tests, create a credentials.json file
# With your client_id, client_secret, username and password
# See example_credentials.json

credentials_file = 'credentials.json'

###########################

filename = os.path.dirname(__file__) + '/' + credentials_file
with open(filename) as f:
    credentials = json.load(f)

CLIENT_ID = credentials["client_id"]
CLIENT_SECRET = credentials["client_secret"]
USERNAME = credentials["username"]
PASSWORD = credentials["password"]

m = Moltin(CLIENT_ID, CLIENT_SECRET)

def test_client_credentials():
    token = m.authenticate()
    expect(len(token) > 0).to.eql(True)


def test_incorrect_client_credentials():
    m = Moltin(client_id="asd",
               client_secret="def")
    m.authenticate.should.throw(RequestError)


def test_user_but_no_pass():
    m.authenticate.when.called_with(username="test").should.throw(FieldTypeError)


def test_pass_but_no_user():
    m.authenticate.when.called_with(password="test").should.throw(FieldTypeError)


def test_user_and_pass_incorrect():
    m.authenticate.when.called_with(username="test", password="test").should.throw(RequestError)


def test_user_and_pass_correct():
    m.authenticate(username=USERNAME, password=PASSWORD)
    expect(len(m.refresh_token) > 0).to.eql(True)

def test_auth_with_incorrect_refresh():
    m.authenticate.when.called_with(refresh_token="test").should.throw(RequestError)

def test_auth_with_correct_refresh():
    m.authenticate(refresh_token=m.refresh_token)
    expect(len(m.access_token) > 0).to.eql(True)