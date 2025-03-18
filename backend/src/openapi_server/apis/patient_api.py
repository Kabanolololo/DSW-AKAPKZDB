# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.patient_api_base import BasePatientApi
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
from typing import List
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.error import Error
from openapi_server.models.patient import Patient


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/patients",
    responses={
        201: {"model": Patient, "description": "Patient added successfully"},
    },
    tags=["Patient"],
    summary="Add a new patient",
    response_model_by_alias=True,
)
async def add_patient(
    patient: Patient = Body(None, description=""),
) -> Patient:
    if not BasePatientApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePatientApi.subclasses[0]().add_patient(patient)


@router.get(
    "/patients/{id}/appointments",
    responses={
        200: {"model": List[Appointment], "description": "List of all appointments for the patient"},
        404: {"model": Error, "description": "Patient not found. The patient with the provided ID does not exist in the system."},
    },
    tags=["Patient"],
    summary="Get all history of a patient",
    response_model_by_alias=True,
)
async def get_patient_history(
    id: Annotated[StrictInt, Field(description="The ID of the patient whose appointment history is to be retrieved")] = Path(..., description="The ID of the patient whose appointment history is to be retrieved"),
) -> List[Appointment]:
    if not BasePatientApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePatientApi.subclasses[0]().get_patient_history(id)


@router.get(
    "/patients/{id}",
    responses={
        200: {"model": Patient, "description": "Details of the patient"},
        404: {"model": Error, "description": "Patient not found"},
    },
    tags=["Patient"],
    summary="Get details of a specific patient",
    response_model_by_alias=True,
)
async def get_patient_id(
    id: StrictInt = Path(..., description=""),
) -> Patient:
    if not BasePatientApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BasePatientApi.subclasses[0]().get_patient_id(id)
