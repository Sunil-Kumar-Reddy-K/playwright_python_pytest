import pytest
import requests
from typing import Dict, Any
from requests import Response
from apis.authtoken_generator import get_auth_token

# Base URL used across all API requests
BASE_URL: str = "https://practice.expandtesting.com/notes/api"

# Global variables
name: str
email: str
password: str = "Test@100"
token: str

@pytest.mark.api
@pytest.mark.all
@pytest.mark.usefixtures("get_token")
def test_create_notes(get_token: str) -> None:
    url: str = f"{BASE_URL}/notes"

    # token = get_token # Use the token from the fixture
    token = get_auth_token() # Use the token from the function directly

    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "x-auth-token": f"{token}"
    }

    data: Dict[str, Any] = {
        "title": "Sample title trial",
        "description": "Sample description trial",
        "category": "Work"
    }

    response: Response = requests.post(url, json=data, headers=headers)

    response_data: Dict[str, Any] = response.json()
    print("Noted Created Response: ", response_data)

    #     Assertions
    assert response.status_code == 200
