from moltin.moltin import Moltin
from moltin.endpoints import BaseEndpoint
from sure import expect
import mock
from .mock_response import mock_response
import sure

m = Moltin("some_id", "some_secret")
endpoint = m.Product


def test_nonexistant_endpoint():
    m.__getattr__.when.called_with("NonexistantEndpoint").should.throw(RuntimeError)


def test_specific_endpoints():
    for e in [m.Product, m.Cart(5)]:
        expect(isinstance(e, BaseEndpoint)).to.eql(True)


@mock.patch("moltin.requests.post")
def test_special_endpoint(mock_post):
    mock_post.return_value = mock_response({"status": "success"})
    cart = m.Cart(5)
    params = {"title": "Item Title"}
    cart.add_item(params)
    mock_post.assert_called_with('https://api.molt.in/v1/carts/5', headers={}, data=params)


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


@mock.patch('moltin.requests.delete')
def test_update(mock_delete):
    result = {"message": "Deleted successfully"}
    mock_delete.return_value = mock_response(result=result)
    expect(endpoint.remove(5)["message"]).to.eql("Deleted successfully")

@mock.patch('moltin.requests')
def test_url_with(mock_request):
    endpoint = BaseEndpoint(mock_request, "cart")
    expect(endpoint._url_with(5)).to.eql("cart/5")