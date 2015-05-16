import json
import os

credentials_file = 'credentials.json'

###########################

filename = os.path.dirname(__file__) + '/' + credentials_file
with open(filename) as f:
    credentials = json.load(f)

CLIENT_ID = credentials["client_id"]
CLIENT_SECRET = credentials["client_secret"]
USERNAME = credentials["username"]
PASSWORD = credentials["password"]