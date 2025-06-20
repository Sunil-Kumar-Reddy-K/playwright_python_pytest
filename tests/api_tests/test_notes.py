import random

import pytest
import requests
from typing import Dict, Any

from requests import Response

# Base URL used across all API requests
BASE_URL: str = "https://practice.expandtesting.com/notes/api"

# Global variables
name: str
email: str
password: str = "Test@100"
token: str

@pytest.mark.api
@pytest.mark.all
def test_notes_api_health_check() -> None:
    url: str = f"{BASE_URL}"

    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }

    response: Response = requests.get(url, headers=headers)

    assert response.status_code == 200

    json_data: Dict[str, Any] = response.json()
    print("Response: ", json_data)

    assert json_data["success"] is True
    assert json_data["status"] == 200
    assert json_data["message"] == "Notes API is Running"

@pytest.mark.api
@pytest.mark.all
def test_new_user_registration() -> None:
    url: str = f"{BASE_URL}/users/register"

    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }

    randon_num: int = random.randint(1000, 9999)

    global password
    data: Dict[str, Any] = {
        "name": "ATP_test",
        "email": f"ATP_test{randon_num}@gmail.com",
        "password": password
    }

    response: Response = requests.post(url, json=data, headers=headers)

    response_data: Dict[str, Any] = response.json()
    print("New user Registration Response: ", response_data)

    #     Assertions

    assert response.status_code == 201

    assert response_data["success"] is True

    global name, email
    if (response_data["message"] == "User account created successfully"):
        name = response_data["data"]["name"]
        email = response_data["data"]["email"]
    else:
        raise Exception("User account not created")

@pytest.mark.api
@pytest.mark.all
def test_user_login() -> None:
    url: str = f"{BASE_URL}/users/login"

    headers: Dict[str, str] = {
        "Content-Type": "application/json"
    }

    data: Dict[str, Any] = {
        "email": email,
        "password": password
    }

    response: Response = requests.post(url, json=data, headers=headers)

    response_data: Dict[str, Any] = response.json()
    print("User Login Response: ", response_data)

    #     Assertions
    assert response.status_code == 200
    assert response_data["success"] is True
    assert response_data["message"] == "Login successful"

    assert response_data["data"]["name"] == name
    assert response_data["data"]["email"] == email
    global token;
    token = response_data["data"]["token"]

    print("User Login Response: ", response_data)
