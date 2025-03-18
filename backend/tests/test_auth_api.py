# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.login import Login  # noqa: F401
from openapi_server.models.token import Token  # noqa: F401
from openapi_server.models.user import User  # noqa: F401


def test_get_profile(client: TestClient):
    """Test case for get_profile

    Get profile of logged-in user
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/auth/profile",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_login_user(client: TestClient):
    """Test case for login_user

    User login (Generate JWT)
    """
    login = {"password":"SecurePassword123","email":"jan.kowalski@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/login",
    #    headers=headers,
    #    json=login,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_register_user(client: TestClient):
    """Test case for register_user

    Register a new user
    """
    user = {"password":"SecurePassword123","surname":"Kowalski","name":"Jan","id":1,"email":"jan.kowalski@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/signup",
    #    headers=headers,
    #    json=user,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

