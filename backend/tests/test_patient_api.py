# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.appointment import Appointment  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.patient import Patient  # noqa: F401


def test_add_patient(client: TestClient):
    """Test case for add_patient

    Add a new patient
    """
    patient = {"phone":"123456789","surname":"Kowalski","date_of_birth":"1985-03-25","name":"Jan","id":1,"email":"jan.kowalski@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/patients",
    #    headers=headers,
    #    json=patient,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_patient_history(client: TestClient):
    """Test case for get_patient_history

    Get all history of a patient
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/patients/{id}/appointments".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_patient_id(client: TestClient):
    """Test case for get_patient_id

    Get details of a specific patient
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/patients/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

