# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.admin_api_base import BaseAdminApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.doctor import Doctor
from openapi_server.models.error import Error
from openapi_server.models.patient import Patient
from openapi_server.models.reschedule_appointment_request import RescheduleAppointmentRequest
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/admin/doctors",
    responses={
        201: {"model": Doctor, "description": "Doctor added successfully"},
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden (insufficient permissions)"},
    },
    tags=["Admin"],
    summary="Add a new doctor",
    response_model_by_alias=True,
)
async def add_doctor(
    doctor: Doctor = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Doctor:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().add_doctor(doctor)


@router.delete(
    "/admin/appointments/{id}",
    responses={
        200: {"description": "Appointment cancelled successfully"},
        401: {"description": "Unauthorized (invalid token)"},
        403: {"description": "Forbidden (insufficient permissions)"},
        404: {"model": Error, "description": "Appointment not found"},
    },
    tags=["Admin"],
    summary="Cancel an appointment",
    response_model_by_alias=True,
)
async def cancel_appointment_admin(
    id: Annotated[StrictInt, Field(description="ID of the appointment to cancel")] = Path(..., description="ID of the appointment to cancel"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().cancel_appointment_admin(id)


@router.delete(
    "/admin/patients/{id}",
    responses={
        200: {"description": "Patient deleted successfully"},
        401: {"description": "Unauthorized (invalid or expired token)"},
        404: {"model": Error, "description": "Patient not found"},
    },
    tags=["Admin"],
    summary="Delete a specific patient",
    response_model_by_alias=True,
)
async def delete_patient(
    id: Annotated[StrictInt, Field(description="The ID of the patient to be deleted")] = Path(..., description="The ID of the patient to be deleted"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().delete_patient(id)


@router.put(
    "/admin/doctors/{id}",
    responses={
        200: {"model": Doctor, "description": "Doctor updated successfully"},
        400: {"description": "Błąd walidacji danych"},
        401: {"description": "Brak autoryzacji"},
        403: {"description": "Brak uprawnień do wykonania tej operacji"},
        404: {"description": "Lekarz o podanym ID nie został znaleziony"},
    },
    tags=["Admin"],
    summary="Edycja danych lekarza",
    response_model_by_alias=True,
)
async def edit_doctor(
    id: Annotated[StrictInt, Field(description="ID lekarza do edytowania")] = Path(..., description="ID lekarza do edytowania"),
    doctor: Doctor = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Doctor:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().edit_doctor(id, doctor)


@router.get(
    "/admin/appointments",
    responses={
        200: {"model": List[Appointment], "description": "Lista wszystkich wizyt"},
        401: {"description": "Brak autoryzacji"},
        403: {"description": "Brak uprawnień do wykonania tej operacji"},
    },
    tags=["Admin"],
    summary="Pobranie wszystkich wizyt",
    response_model_by_alias=True,
)
async def get_all_appointments(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[Appointment]:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().get_all_appointments()


@router.get(
    "/admin/doctors",
    responses={
        200: {"model": List[Doctor], "description": "List of all doctors"},
        401: {"description": "Unauthorized (invalid token)"},
        403: {"description": "Forbidden (insufficient permissions)"},
    },
    tags=["Admin"],
    summary="Get all doctors",
    response_model_by_alias=True,
)
async def get_all_doctors_admin(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[Doctor]:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().get_all_doctors_admin()


@router.get(
    "/admin/patients",
    responses={
        200: {"model": List[Patient], "description": "A list of all patients"},
        401: {"description": "Unauthorized (invalid or expired token)"},
    },
    tags=["Admin"],
    summary="Get a list of all patients",
    response_model_by_alias=True,
)
async def get_all_patients(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[Patient]:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().get_all_patients()


@router.get(
    "/admin/patients/{id}",
    responses={
        200: {"model": Patient, "description": "Details of the patient"},
        401: {"description": "Unauthorized (invalid or expired token)"},
        404: {"model": Error, "description": "Patient not found"},
    },
    tags=["Admin"],
    summary="Get details of a specific patient",
    response_model_by_alias=True,
)
async def get_patient_details(
    id: Annotated[StrictInt, Field(description="The ID of the patient whose details are to be retrieved")] = Path(..., description="The ID of the patient whose details are to be retrieved"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Patient:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().get_patient_details(id)


@router.put(
    "/admin/appointments/{id}/reschedule",
    responses={
        200: {"model": Appointment, "description": "Appointment rescheduled successfully"},
        400: {"model": Error, "description": "Invalid input (e.g., past date or doctor unavailable)"},
        401: {"description": "Unauthorized (invalid token)"},
        403: {"description": "Forbidden (insufficient permissions)"},
        404: {"model": Error, "description": "Appointment not found"},
    },
    tags=["Admin"],
    summary="Reschedule an appointment",
    response_model_by_alias=True,
)
async def reschedule_appointment(
    id: Annotated[StrictInt, Field(description="ID of the appointment to reschedule")] = Path(..., description="ID of the appointment to reschedule"),
    reschedule_appointment_request: RescheduleAppointmentRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Appointment:
    if not BaseAdminApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAdminApi.subclasses[0]().reschedule_appointment(id, reschedule_appointment_request)
