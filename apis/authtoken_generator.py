import requests


# Base URL used across all API requests
BASE_URL: str = "https://practice.expandtesting.com/notes/api"

# Global variables
name: str = "ATP_test"
email: str = "atp_test8752@gmail.com"
password: str = "Test@100"
token: str


def get_auth_token() -> str:
    url = f"{BASE_URL}/users/login"
    headers = {"Content-Type": "application/json"}
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    return response.json()["data"]["token"]