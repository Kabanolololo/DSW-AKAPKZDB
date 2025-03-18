# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import List
from typing_extensions import Annotated
from openapi_server.models.appointment import Appointment
from openapi_server.models.error import Error
from openapi_server.models.patient import Patient


class BasePatientApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BasePatientApi.subclasses = BasePatientApi.subclasses + (cls,)
    async def add_patient(
        self,
        patient: Patient,
    ) -> Patient:
        ...


    async def get_patient_history(
        self,
        id: Annotated[StrictInt, Field(description="The ID of the patient whose appointment history is to be retrieved")],
    ) -> List[Appointment]:
        ...


    async def get_patient_id(
        self,
        id: StrictInt,
    ) -> Patient:
        ...
