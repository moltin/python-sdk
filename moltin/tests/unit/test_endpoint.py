from moltin.moltin import *
from sure import expect
import mock
from . mock_response import mock_response
import sure

m = Moltin("some_id", "some_secret")
endpoint = m.Product


def get_endpoint_response():
    return


def test_nonexistant_endpoint():
    m.__getattr__.when.called_with("NonexistantEndpoint").should.throw(RuntimeError)


def test_specific_endpoint():
    expect(isinstance(endpoint, BaseEndpoint)).to.eql(True)


@mock.patch('moltin.requests.get')
def test_find(mock_get):
    mock_get.return_value = mock_response(result={"id": 5})
    expect(endpoint.find(5)["id"]).to.eql(5)

@mock.patch('moltin.requests.get')
def test_find_by(mock_get):
    mock_get.return_value = mock_response(result={"id": 5, "slug": "someslug"})
    expect(endpoint.find_by({"slug": "someslug"})["id"]).to.eql(5)


@mock.patch('moltin.requests.get')
def test_list(mock_get):
    mock_get.return_value = mock_response(result=[{"id": 5}, {"id": 6}])
    expect(endpoint.list()[0]["id"]).to.eql(5)


@mock.patch('moltin.requests.post')
def test_create(mock_post):
    params = {"title": "Product Title", "quantity": 3}
    result = {"id": 5}
    result.update(params)
    mock_post.return_value = mock_response(result=result)
    expect(endpoint.create(params)["id"]).to.eql(5)

@mock.patch('moltin.requests.put')
def test_update(mock_put):
    params = {"title": "New product Title", "quantity": 4}
    result = {"message": "Updated successfully"}
    mock_put.return_value = mock_response(result=result)
    expect(endpoint.update(5, params)["message"]).to.eql("Updated successfully")