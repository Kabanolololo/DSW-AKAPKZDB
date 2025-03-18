# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field, StrictInt
from typing import List
from typing_extensions import Annotated
from openapi_server.models.doctor import Doctor
from openapi_server.models.error import Error
from openapi_server.models.get_doctor_available_slots200_response_inner import GetDoctorAvailableSlots200ResponseInner


class BaseDoctorApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDoctorApi.subclasses = BaseDoctorApi.subclasses + (cls,)
    async def get_all_doctors(
        self,
    ) -> List[Doctor]:
        ...


    async def get_doctor_available_slots(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the doctor whose available slots are to be retrieved")],
        var_date: Annotated[date, Field(description="The date for which to retrieve available slots (format YYYY-MM-DD)")],
    ) -> List[GetDoctorAvailableSlots200ResponseInner]:
        ...


    async def get_doctor_id(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the doctor whose details are to be retrieved")],
    ) -> Doctor:
        ...
