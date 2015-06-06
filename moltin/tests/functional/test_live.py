# -*- coding: utf-8 -*-

import json
import os
from moltin.moltin import Moltin
from sure import expect
import warnings

# To run the live functional tests, create a file
# called credentials.json in the format:
# {
#   "client_id": "YOUR_CLIENT_ID",
#   "client_secret": "YOUR_CLIENT_SECRET"
# }
#
#
# Or load them from env variables

CREDENTIALS_PATH = 'credentials.json'

#################


def read_json_file(path):
    base = os.path.dirname(os.path.realpath(__file__)) + "/"
    real_path = base + path

    with open(real_path) as f:
        result = json.load(f)

    return result

# If loading from credentials file:
try:
    credentials = read_json_file(CREDENTIALS_PATH)

    # If loading from env or elsewhere:
    # credentials = {"client_id": YOUR_CLIENT_ID, "client_secret": YOUR_SECRET}

    m = Moltin(credentials["client_id"], credentials["client_secret"])
    product = m.Product

    def test_authenticate():
        token = m.authenticate()
        expect(len(token.token) > 0).to.eql(True)

    def test_authenticate_with_user():
        token, refresh = m.authenticate(username=credentials["username"], password=credentials["password"])
        expect(len(refresh.token) > 0).to.eql(True)
        expect(len(token.token) > 0).to.eql(True)

    def test_endpoints():
        for endpoint, val in m.endpoints.items():
            endpoint = getattr(m, endpoint)
            endpoint.list()
except IOError:
    warnings.warn("Create a credentials.json file to run live tests")

