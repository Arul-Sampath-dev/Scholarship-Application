class DomainException(Exception):
    status_code: int

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidCredentials(Exception):
    pass


class InvalidPasswordAndConfirmation(Exception):
    pass


class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass
