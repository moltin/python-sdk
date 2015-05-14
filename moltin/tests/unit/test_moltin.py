from moltin.moltin import Moltin
from sure import expect

def test_authenticate():
    m = Moltin(client_id="njE59xf5KgjkGuH9Wqwv69Qdp2DbraJzBXAcKwzV",
               client_secret="HzDwpH0pNfLEgw9gWOSMsIrvVrST9QaoVB83kG7L")
    auth = m.authenticate()
    print auth