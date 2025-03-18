# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.auth_api_base import BaseAuthApi
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
from typing import Any
from openapi_server.models.error import Error
from openapi_server.models.login import Login
from openapi_server.models.token import Token
from openapi_server.models.user import User
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/auth/profile",
    responses={
        200: {"model": User, "description": "User profile data"},
        401: {"model": Error, "description": "Unauthorized. Token is missing or invalid."},
    },
    tags=["Auth"],
    summary="Get profile of logged-in user",
    response_model_by_alias=True,
)
async def get_profile(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> User:
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().get_profile()


@router.post(
    "/auth/login",
    responses={
        200: {"model": Token, "description": "Login successful, returns JWT token"},
        401: {"model": Error, "description": "Invalid credentials"},
    },
    tags=["Auth"],
    summary="User login (Generate JWT)",
    response_model_by_alias=True,
)
async def login_user(
    login: Login = Body(None, description=""),
) -> Token:
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().login_user(login)


@router.post(
    "/auth/signup",
    responses={
        201: {"model": User, "description": "User created successfully"},
        400: {"description": "Invalid input (e.g., missing data, invalid email)"},
    },
    tags=["Auth"],
    summary="Register a new user",
    response_model_by_alias=True,
)
async def register_user(
    user: User = Body(None, description=""),
) -> User:
    """Allows a new user to register by providing their details."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().register_user(user)
