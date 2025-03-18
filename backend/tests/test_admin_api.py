# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.appointment import Appointment  # noqa: F401
from openapi_server.models.doctor import Doctor  # noqa: F401
from openapi_server.models.error import Error  # noqa: F401
from openapi_server.models.patient import Patient  # noqa: F401
from openapi_server.models.reschedule_appointment_request import RescheduleAppointmentRequest  # noqa: F401


def test_add_doctor(client: TestClient):
    """Test case for add_doctor

    Add a new doctor
    """
    doctor = {"phone":"987654321","surname":"Nowak","name":"Anna","specialization":"Cardiologist","id":1,"email":"anna.nowak@clinic.com"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/admin/doctors",
    #    headers=headers,
    #    json=doctor,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cancel_appointment_admin(client: TestClient):
    """Test case for cancel_appointment_admin

    Cancel an appointment
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/admin/appointments/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_patient(client: TestClient):
    """Test case for delete_patient

    Delete a specific patient
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/admin/patients/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_edit_doctor(client: TestClient):
    """Test case for edit_doctor

    Edycja danych lekarza
    """
    doctor = {"phone":"987654321","surname":"Nowak","name":"Anna","specialization":"Cardiologist","id":1,"email":"anna.nowak@clinic.com"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/admin/doctors/{id}".format(id=56),
    #    headers=headers,
    #    json=doctor,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_all_appointments(client: TestClient):
    """Test case for get_all_appointments

    Pobranie wszystkich wizyt
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/admin/appointments",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_all_doctors_admin(client: TestClient):
    """Test case for get_all_doctors_admin

    Get all doctors
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/admin/doctors",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_all_patients(client: TestClient):
    """Test case for get_all_patients

    Get a list of all patients
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/admin/patients",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_patient_details(client: TestClient):
    """Test case for get_patient_details

    Get details of a specific patient
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/admin/patients/{id}".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_reschedule_appointment(client: TestClient):
    """Test case for reschedule_appointment

    Reschedule an appointment
    """
    reschedule_appointment_request = openapi_server.RescheduleAppointmentRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/admin/appointments/{id}/reschedule".format(id=56),
    #    headers=headers,
    #    json=reschedule_appointment_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

