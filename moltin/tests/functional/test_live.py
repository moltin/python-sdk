# -*- coding: utf-8 -*-

import json
import os
from moltin.moltin import Moltin
from sure import expect

def read_json_file(path):
    base = os.path.dirname(os.path.realpath(__file__)) + "/"
    real_path = base + path
    with open(real_path) as f:
        result = json.load(f)

    return result

# To run the live functional tests, create a file
# called credentials.json in the format:
# {
#   "client_id": "YOUR_CLIENT_ID",
#   "client_secret": "YOUR_CLIENT_SECRET"
# }
# Or load them from env variables

CREDENTIALS_PATH = 'credentials.json'

# If loading from credentials file:
credentials = read_json_file(CREDENTIALS_PATH)

# If loading from env or elsewhere:
# credentials = {"client_id": YOUR_CLIENT_ID, "client_secret": YOUR_SECRET}


m = Moltin(credentials["client_id"], credentials["client_secret"])
m.authenticate()
product = m.Product


def test_create():
    print product.find(5)
    print product.find_by({"title": "Hello"})
    print product.update(5, {"title": "Hello"})