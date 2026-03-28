import requests

def test_http_status():
    response = requests.get('https://httpbin.org/status/200')
    assert response.status_code == 200

def test_json_response():
    response = requests.get('https://httpbin.org/json')
    assert response.status_code == 200
    assert 'slideshow' in response.json()

    import requests

response = requests.get('https://httpbin.org/get')

print(f"Status Code: {response.status_code}")
assert response.status_code == 200
print(f"Response received: {bool(response)}")
print(f"Headers: {response.headers}")
print(f"Request URL: {response.url}")