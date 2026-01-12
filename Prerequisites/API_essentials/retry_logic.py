# Implement retry logic for failed API calls.

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# define the retry strategy
retry_strategy = Retry(
    total=4,  # maximum number of retries
    backoff_factor=2,
    status_forcelist=[
        429,
        500,
        502,
        503,
        504,
    ],  # the HTTP status codes to retry on
)

# create an HTTP adapter with the retry strategy and mount it to the session
adapter = HTTPAdapter(max_retries=retry_strategy)

# create a new session object
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

# make a request using the session object
response = session.get("https://example.com")
if response.status_code == 200:
    print(f"SUCCESS: {response.json}")
else:
    print(f"FAILED with status {response.status_code}")