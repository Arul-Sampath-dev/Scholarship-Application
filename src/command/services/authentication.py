from typing import cast
from uuid import UUID

from src.api.shemas.authentication import FromProvider
from src.command.commands.authentication import (
    CreateUser,
    CreateUserWithConfirm,
    GetUserContext,
    LoginUser,
    ProviderCreate,
    Role,
    Token,
    UserContext,
    UserHasProvider,
    UserPayload,
)
from src.command.repositories.authentication import AuthenticationRepository
from src.core.authentication import JWTHandler, PasswordHandler
from src.database import DBManager
from src.exceptions import (
    InvalidCredentialsError,
    InvalidPasswordAndConfirmationError,
    UserAlreadyExistsError,
)


class AuthenticationService:
    def __init__(
        self,
        auth_repo: AuthenticationRepository,
        password_handler: PasswordHandler,
        jwt_handler: JWTHandler,
    ):
        self.auth_repo = auth_repo
        self.password_handler = password_handler
        self.jwt_handler = jwt_handler

    def register_user(self, cmd: CreateUserWithConfirm) -> Token:
        if cmd.password != cmd.confirm_password:
            raise InvalidPasswordAndConfirmationError()
        user = self.auth_repo.get_user_context(GetUserContext(email=cmd.email))
        # user = self.auth_repo.get_user_by_email(cmd.email)

        if user:
            raise UserAlreadyExistsError()

        user = self.auth_repo.create_user(
            CreateUser(
                username=cmd.username,
                email=cmd.email,
                password=self.password_handler.hash_password(cmd.password),
                role=Role.STUDENT,
                email_verified=False,
            )
        )

        token = self.jwt_handler.encode_jwt(
            UserPayload(
                user_id=cast(UUID, user.user_id),
                username=user.username,
                email=user.email,
                role=user.role,
                type="access",
                email_verified=user.email_verified,
            )
        )
        return Token(access_token=token)

    def login(self, cmd: LoginUser) -> Token:
        # user = self.auth_repo.get_user_context(GetUserContext(email=cmd.email))
        # Here i need to check the password for that im fetch all the user data using get_user_by_email
        user = self.auth_repo.get_user_by_email(cmd.email)

        if not user or not self.password_handler.verify_password(
            cmd.password, cast(str, user.password)
        ):
            raise InvalidCredentialsError()

        # need to convert into token and send to api layer

        token = self.jwt_handler.encode_jwt(
            UserPayload(
                user_id=cast(UUID, user.user_id),
                username=user.username,
                email=user.email,
                role=user.role,
                type="access",
                email_verified=user.email_verified,
            )
        )

        return Token(access_token=token)

    def login_via_oauth(self, cmd: FromProvider) -> Token:
        # existing_user = self.auth_repo.get_user_by_email(cmd.email)
        existing_user = self.auth_repo.get_user_context(GetUserContext(email=cmd.email))
        # todo: in here i done the account validation using GetUserContext i need to change it. I need to check the account hasn't been deleted
        if existing_user:
            # i need to check if the user has a provider
            if (
                self.auth_repo.get_provider(
                    UserHasProvider(
                        user_id=cast(UUID, existing_user.user_id),
                        provider_name=cmd.provider,
                    )
                )
                is None
            ):
                self.auth_repo.create_provider(
                    ProviderCreate(
                        user_id=cast(UUID, existing_user.user_id),
                        provider_name=cmd.provider,
                    )
                )

            token = self.jwt_handler.encode_jwt(
                UserPayload(
                    user_id=cast(UUID, existing_user.user_id),
                    username=existing_user.username,
                    email=existing_user.email,
                    role=existing_user.role,
                    type="access",
                    email_verified=existing_user.email_verified,
                )
            )
            return Token(
                access_token=token,
            )

        user_context = self.auth_repo.create_user(
            CreateUser(
                username=cmd.username,
                email=cmd.email,
                role=Role.STUDENT,
                email_verified=True,
            )
        )

        self.auth_repo.create_provider(
            ProviderCreate(
                user_id=cast(UUID, user_context.user_id),
                provider_name=cmd.provider,
            )
        )

        token = self.jwt_handler.encode_jwt(
            UserPayload(
                user_id=cast(UUID, user_context.user_id),
                username=user_context.username,
                email=user_context.email,
                role=user_context.role,
                type="access",
                email_verified=user_context.email_verified,
            )
        )

        return Token(
            access_token=token,
        )

    def get_user_by_token(self, token: str) -> UserContext:
        payload = self.jwt_handler.decode_jwt(token)
        return UserContext(
            user_id=cast(UUID, payload.user_id),
            username=payload.username,
            email=payload.email,
            role=payload.role,
            email_verified=payload.email_verified,
        )


if __name__ == "__main__":
    db = DBManager()
    auth_repo = AuthenticationRepository(db)
    password_handler = PasswordHandler()
    jwt_handler = JWTHandler()
    auth_service = AuthenticationService(auth_repo, password_handler, jwt_handler)

    # auth_service.register_user(
    #     CreateUserWithConfirm(
    #         username="arul",
    #         email="arulsampathcyr@gmail.com",
    #         password="123",
    #         confirm_password="123",
    #     )
    # )

    # print(
    #     auth_service.login(
    #         LoginUser(
    #             email="arulsampathcyr@gmail.com",
    #             password="123",
    #         )
    #     )
    # )
