# Build a small helper function for authenticated API requests.

import requests
from requests.auth import HTTPBasicAuth
import os
import json
from dotenv import load_dotenv 

load_dotenv()

# Access credentials using environment variables
username= os.getenv("user")
password=os.getenv("token")

url = 'https://api.github.com/user'

# Making a get request
response = requests.get(url, auth=HTTPBasicAuth(username, password))

# Printing the information received from response object in readable json
if response.status_code == 200:
    data = response.json()
    pretty_json = json.dumps(data, indent=4, sort_keys=True)
    print(pretty_json)