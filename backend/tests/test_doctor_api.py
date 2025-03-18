# coding: utf-8

from fastapi.testclient import TestClient


from datetime import date  # noqa: F401
from pydantic import Field, StrictInt  # noqa: F401
from typing import List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.doctor import Doctor  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.get_doctor_available_slots200_response_inner import GetDoctorAvailableSlots200ResponseInner  # noqa: F401


def test_get_all_doctors(client: TestClient):
    """Test case for get_all_doctors

    Retrieve a list of all doctors
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/doctors",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_doctor_available_slots(client: TestClient):
    """Test case for get_doctor_available_slots

    Get available slots for a specific doctor on a given date
    """
    params = [("var_date", '2013-10-20')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/doctors/{id}/available-slots".format(id=56),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_doctor_id(client: TestClient):
    """Test case for get_doctor_id

    Get details of a specific doctor
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/doctors/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

