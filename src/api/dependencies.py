from typing import Annotated

from fastapi import Depends

from src.command.services.authentication import AuthenticationService
from src.dependencies import auth_service


def get_auth_service() -> AuthenticationService:
    return auth_service


type AuthenticationDependency = Annotated[
    AuthenticationService, Depends(get_auth_service)
]
