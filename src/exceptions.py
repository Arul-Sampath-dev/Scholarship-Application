"""
Why i dont use status codes here.
Why we need to map the status code for the respective exceptions in exception_registry.py in api layer
 - API layer is the responsible for request, response and status codes for that we used the exception_registry.py for mapping.
 - why not here: Because we want to keep the exceptions clean and separate from the status codes.
 - Every layer has its own responsibility and status codes should be handled at the API layer.

 Architecture:
     Repository/ Service -> Raise the Exceptions
     In main -> Catch the Exceptions using exception_handler(we declared universal global exception handler) - This enables Global exception handling.
     In exception_handler -> Map the Exceptions to status codes(we get the status code from the exception registry)
     In exception_handler -> Return the status code and message to the client
"""

from typing import Optional

# Domain Exceptions
"""
    Base Exception for all domain exceptions.
"""


class DomainException(Exception):
    error_code = "DOMAIN_ERROR"
    message = "Internal Server Errror"

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
        super().__init__(self.message)


# Authentication Exceptions
"""
    Authentication Exceptions - Raised when authentication fails or is not provided.
"""


class AuthenticationExceptions(DomainException):
    error_code = "AUTHENTICATION_ERROR"
    message = "Authentication failed"


class InvalidCredentialsError(AuthenticationExceptions):
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid Email or Password"


class InvalidTokenError(AuthenticationExceptions):
    error_code = "INVALID_TOKEN"
    message = "Invalid Authentication Token"


class ExpiredTokenError(AuthenticationExceptions):
    error_code = "EXPIRED_TOKEN"
    message = "Authentication Token is Expired"


class MissingTokenError(AuthenticationExceptions):
    error_code = "MISSING_TOKEN"
    message = "Authentication Token is missing"


#   Not Found Exceptions
"""
    Not Found Exceptions - Raised when a resource is not found.
"""


class NotFoundExceptions(DomainException):
    error_code = "NOT_FOUND"
    _entity = "Resource"

    def __init__(self):
        self.message = f"{self._entity} not found"
        super().__init__(self.message)


class UserNotFoundError(NotFoundExceptions):
    _entity = "User"


# conflict Exceptions:
"""
    Conflict Exceptions - Raised when a conflict occurs, such as a duplicate resource.
"""


class ConflictExceptios(DomainException):
    pass


class UserAlreadyExistsError(ConflictExceptios):
    error_code = "USER_ALREAD_EXISTS"
    message = "User Already Exists"


#   Validation Exceptions
class ValidationException(DomainException):
    error_code = "VALIDATION_ERROR"
    message = "Validation failed"


class InvalidPasswordAndConfirmationError(ValidationException):
    error_code = "INVALID_PASSWORD_CONFIRMATION"
    message = "Password and confirmation do not match"
