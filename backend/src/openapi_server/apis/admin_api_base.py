# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.doctor import Doctor
from openapi_server.models.error import Error
from openapi_server.models.patient import Patient
from openapi_server.models.reschedule_appointment_request import RescheduleAppointmentRequest
from openapi_server.security_api import get_token_bearerAuth

class BaseAdminApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAdminApi.subclasses = BaseAdminApi.subclasses + (cls,)
    async def add_doctor(
        self,
        doctor: Doctor,
    ) -> Doctor:
        ...


    async def cancel_appointment_admin(
        self,
        id: Annotated[StrictInt, Field(description="ID of the appointment to cancel")],
    ) -> None:
        ...


    async def delete_patient(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the patient to be deleted")],
    ) -> None:
        ...


    async def edit_doctor(
        self,
        id: Annotated[StrictInt, Field(description="ID lekarza do edytowania")],
        doctor: Doctor,
    ) -> Doctor:
        ...


    async def get_all_appointments(
        self,
    ) -> List[Appointment]:
        ...


    async def get_all_doctors_admin(
        self,
    ) -> List[Doctor]:
        ...


    async def get_all_patients(
        self,
    ) -> List[Patient]:
        ...


    async def get_patient_details(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the patient whose details are to be retrieved")],
    ) -> Patient:
        ...


    async def reschedule_appointment(
        self,
        id: Annotated[StrictInt, Field(description="ID of the appointment to reschedule")],
        reschedule_appointment_request: RescheduleAppointmentRequest,
    ) -> Appointment:
        ...
