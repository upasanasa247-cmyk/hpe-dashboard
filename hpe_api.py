import requests

CLIENT_ID = "d22559cd-b16e-41a0-8294-a3961d1fd14a"
CLIENT_SECRET = "bd2152ef9e224545ad28bf29f46137bf"

TOKEN_URL = "https://api.greenlake.hpe.com/identity/v1/token"

def get_token():
    response = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    response.raise_for_status()
    return response.json()["access_token"]


def get_hpe_devices():
    token = get_token()

    url = "https://api.greenlake.hpe.com/v1/inventory/devices"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return response.json()