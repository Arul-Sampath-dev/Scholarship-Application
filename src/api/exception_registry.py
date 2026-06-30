"""
This module provides the exception registry for the API.
    - In this module we map the status codes to the respected exceptions.
"""

from http import HTTPStatus
from typing import Type

import src.exceptions as exc

exception_registry: dict[Type[exc.DomainException], HTTPStatus] = {
    exc.AuthenticationExceptions: HTTPStatus.UNAUTHORIZED,  # 401
    exc.ValidationException: HTTPStatus.BAD_REQUEST,  # 400
    exc.NotFoundExceptions: HTTPStatus.NOT_FOUND,  # 404
    exc.ConflictExceptios: HTTPStatus.CONFLICT,  # 409
}
