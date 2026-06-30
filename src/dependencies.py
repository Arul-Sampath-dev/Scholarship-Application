"""
This module provides dependency injection for the application.
In here i creates a singleton objects for ther services.
- Services needed repository, db singletons.
"""

from src.command.repositories.authentication import AuthenticationRepository
from src.command.repositories.provider import ProviderRepository
from src.command.services.authentication import AuthenticationService
from src.core.authentication import JWTHandler, PasswordHandler
from src.database import DBManager

db = DBManager()
auth_repo = AuthenticationRepository(db_manager=db)
provider_repo = ProviderRepository(db_manager=db)

password_handler = PasswordHandler()
jwt_handler = JWTHandler()
auth_service = AuthenticationService(
    auth_repo=auth_repo,
    password_handler=password_handler,
    jwt_handler=jwt_handler,
    provider_repo=provider_repo,
)
