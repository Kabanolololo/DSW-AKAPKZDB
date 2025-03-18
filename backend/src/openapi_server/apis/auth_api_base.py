# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any
from openapi_server.models.error import Error
from openapi_server.models.login import Login
from openapi_server.models.token import Token
from openapi_server.models.user import User
from openapi_server.security_api import get_token_bearerAuth

class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses = BaseAuthApi.subclasses + (cls,)
    async def get_profile(
        self,
    ) -> User:
        ...


    async def login_user(
        self,
        login: Login,
    ) -> Token:
        ...


    async def register_user(
        self,
        user: User,
    ) -> User:
        """Allows a new user to register by providing their details."""
        ...
