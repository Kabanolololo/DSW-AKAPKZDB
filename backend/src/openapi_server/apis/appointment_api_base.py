# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.error import Error


class BaseAppointmentApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAppointmentApi.subclasses = BaseAppointmentApi.subclasses + (cls,)
    async def add_appointment(
        self,
        appointment: Appointment,
    ) -> Appointment:
        ...


    async def cancel_appointment(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the appointment to cancel")],
    ) -> None:
        ...


    async def edit_appointment(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the appointment to edit")],
        appointment: Appointment,
    ) -> Appointment:
        ...


    async def get_appointment_details(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the appointment to retrieve details for")],
    ) -> Appointment:
        ...
