# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.appointment_api_base import BaseAppointmentApi
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
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.error import Error


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/appointments",
    responses={
        201: {"model": Appointment, "description": "Appointment added successfully"},
        400: {"model": Error, "description": "Invalid input. Missing or incorrect data."},
        404: {"model": Error, "description": "Patient or doctor not found"},
    },
    tags=["Appointment"],
    summary="Add a new appointment",
    response_model_by_alias=True,
)
async def add_appointment(
    appointment: Appointment = Body(None, description=""),
) -> Appointment:
    if not BaseAppointmentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAppointmentApi.subclasses[0]().add_appointment(appointment)


@router.delete(
    "/appointments/{id}",
    responses={
        200: {"description": "Appointment cancelled successfully"},
        400: {"model": Error, "description": "Invalid request (e.g., the appointment could not be cancelled)"},
        404: {"model": Error, "description": "Appointment not found"},
    },
    tags=["Appointment"],
    summary="Cancel a specific appointment",
    response_model_by_alias=True,
)
async def cancel_appointment(
    id: Annotated[StrictInt, Field(description="The ID of the appointment to cancel")] = Path(..., description="The ID of the appointment to cancel"),
) -> None:
    if not BaseAppointmentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAppointmentApi.subclasses[0]().cancel_appointment(id)


@router.put(
    "/appointments/{id}",
    responses={
        200: {"model": Appointment, "description": "Appointment updated successfully"},
        400: {"model": Error, "description": "Invalid request (e.g., invalid data format)"},
        404: {"model": Error, "description": "Appointment not found"},
    },
    tags=["Appointment"],
    summary="Edit details of an existing appointment",
    response_model_by_alias=True,
)
async def edit_appointment(
    id: Annotated[StrictInt, Field(description="The ID of the appointment to edit")] = Path(..., description="The ID of the appointment to edit"),
    appointment: Appointment = Body(None, description=""),
) -> Appointment:
    if not BaseAppointmentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAppointmentApi.subclasses[0]().edit_appointment(id, appointment)


@router.get(
    "/appointments/{id}",
    responses={
        200: {"model": Appointment, "description": "Details of the appointment"},
        404: {"model": Error, "description": "Appointment not found"},
    },
    tags=["Appointment"],
    summary="Get details of a specific appointment",
    response_model_by_alias=True,
)
async def get_appointment_details(
    id: Annotated[StrictInt, Field(description="The ID of the appointment to retrieve details for")] = Path(..., description="The ID of the appointment to retrieve details for"),
) -> Appointment:
    if not BaseAppointmentApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAppointmentApi.subclasses[0]().get_appointment_details(id)
