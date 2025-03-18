# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.appointment import Appointment  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401


def test_add_appointment(client: TestClient):
    """Test case for add_appointment

    Add a new appointment
    """
    appointment = {"doctor_id":1,"patient_id":1,"appointment_date":"2025-03-20T14:00:00Z","id":1,"status":"scheduled"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/appointments",
    #    headers=headers,
    #    json=appointment,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cancel_appointment(client: TestClient):
    """Test case for cancel_appointment

    Cancel a specific appointment
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/appointments/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_edit_appointment(client: TestClient):
    """Test case for edit_appointment

    Edit details of an existing appointment
    """
    appointment = {"doctor_id":1,"patient_id":1,"appointment_date":"2025-03-20T14:00:00Z","id":1,"status":"scheduled"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/appointments/{id}".format(id=56),
    #    headers=headers,
    #    json=appointment,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_appointment_details(client: TestClient):
    """Test case for get_appointment_details

    Get details of a specific appointment
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/appointments/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

