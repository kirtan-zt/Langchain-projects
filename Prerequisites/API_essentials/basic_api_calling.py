# Call a sample public API and print formatted results.

import requests

url='https://tutorial.djangogirls.org/en/installation/'

def make_request_func(url_path):
    r=requests.get(url_path)
    return r

response = make_request_func(url)

print(f"Status code returned from url: {response.status_code}")
print(f"JSON on the url: {response.json}")
print(f"Headers of url: {response.headers['content-type']}")