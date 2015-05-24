from moltin.moltin import *
from sure import expect
import mock
from mock_response import mock_response
import sure

m = Moltin("some_id", "some_secret")
endpoint = BaseEndpoint(Request("v1"), "product")


def get_endpoint_response():
    return


def test_nonexistant_endpoint():
    m.__getattr__.when.called_with("NonexistantEndpoint").should.throw(RuntimeError)


def test_specific_endpoint():
    checkout = m.Checkout
    expect(isinstance(checkout, BaseEndpoint)).to.eql(True)


@mock.patch('moltin.requests.get')
def test_base_endpoint(mock_get):
    mock_get.return_value = mock_response(result={"id": 15})
    expect(endpoint.find(5)["id"]).to.eql(15)