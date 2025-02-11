import requests

def send_request(endpoint, params):
    base_url = "https://api.gateio.ws/api/v4"
    url = f"{base_url}{endpoint}"
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None
