from moltin.endpoints import *
from moltin.moltin import Moltin
from sure import expect
import sure

m = Moltin("some_id", "some_secret")


def test_nonexistant_endpoint():
    m.__getattr__.when.called_with("NonexistantEndpoint").should.throw(RuntimeError)

def test_endpoint():
    checkout = m.Checkout
    expect(type(checkout) is BaseEndpoint).to.eql(True)
