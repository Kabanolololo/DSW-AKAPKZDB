# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.doctor_api_base import BaseDoctorApi
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
from datetime import date
from pydantic import Field, StrictInt
from typing import List
from typing_extensions import Annotated
from openapi_server.models.doctor import Doctor
from openapi_server.models.error import Error
from openapi_server.models.get_doctor_available_slots200_response_inner import GetDoctorAvailableSlots200ResponseInner


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/doctors",
    responses={
        200: {"model": List[Doctor], "description": "A list of all doctors"},
    },
    tags=["Doctor"],
    summary="Retrieve a list of all doctors",
    response_model_by_alias=True,
)
async def get_all_doctors(
) -> List[Doctor]:
    if not BaseDoctorApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDoctorApi.subclasses[0]().get_all_doctors()


@router.get(
    "/doctors/{id}/available-slots",
    responses={
        200: {"model": List[GetDoctorAvailableSlots200ResponseInner], "description": "A list of available slots for the doctor on the given date"},
        400: {"model": Error, "description": "Bad request due to incorrect date format or missing parameters"},
        404: {"model": Error, "description": "Doctor or available slots not found"},
    },
    tags=["Doctor"],
    summary="Get available slots for a specific doctor on a given date",
    response_model_by_alias=True,
)
async def get_doctor_available_slots(
    id: Annotated[StrictInt, Field(description="The ID of the doctor whose available slots are to be retrieved")] = Path(..., description="The ID of the doctor whose available slots are to be retrieved"),
    var_date: Annotated[date, Field(description="The date for which to retrieve available slots (format YYYY-MM-DD)")] = Query(None, description="The date for which to retrieve available slots (format YYYY-MM-DD)", alias="date"),
) -> List[GetDoctorAvailableSlots200ResponseInner]:
    if not BaseDoctorApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDoctorApi.subclasses[0]().get_doctor_available_slots(id, var_date)


@router.get(
    "/doctors/{id}",
    responses={
        200: {"model": Doctor, "description": "Details of the doctor"},
        404: {"model": Error, "description": "Doctor not found"},
    },
    tags=["Doctor"],
    summary="Get details of a specific doctor",
    response_model_by_alias=True,
)
async def get_doctor_id(
    id: Annotated[StrictInt, Field(description="The ID of the doctor whose details are to be retrieved")] = Path(..., description="The ID of the doctor whose details are to be retrieved"),
) -> Doctor:
    if not BaseDoctorApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDoctorApi.subclasses[0]().get_doctor_id(id)
