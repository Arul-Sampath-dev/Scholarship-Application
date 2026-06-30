from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.hash import argon2  # type: ignore

from src.command.commands.authentication import Role, UserPayload
from src.exceptions import InvalidTokenError
from src.settings import settings


class PasswordHandler:
    def hash_password(self, password: str) -> str:
        return argon2.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return argon2.verify(password, hashed_password)


class JWTHandler:
    def encode_jwt(self, cmd: UserPayload) -> str:
        payload = cmd.model_dump(mode="json")
        payload["exp"] = datetime.now() + timedelta(seconds=settings.jwt.seconds)
        return jwt.encode(
            payload,
            key=settings.jwt.secret,
            algorithm=settings.jwt.algorithm,
        )

    def decode_jwt(self, token: str) -> UserPayload:
        try:
            return UserPayload(
                **jwt.decode(
                    token, key=settings.jwt.secret, algorithms=[settings.jwt.algorithm]
                )
            )
        except JWTError:
            raise InvalidTokenError()


if __name__ == "__main__":
    # password_handler = PasswordHandler()
    # hashed_password = password_handler.hash_password("123")
    # print(hashed_password)
    # print(password_handler.verify_password("123", hashed_password))

    jwt_handler = JWTHandler()
    token = jwt_handler.encode_jwt(
        UserPayload(
            user_id=UUID("fe0436f9-d0fa-4f3d-84e1-cc438e302e91"),
            username="Arul S",
            email="arulsampathcyr@gmail.com",
            role=Role.STUDENT,
            type="access_token",
            email_verified=False,
        )
    )

    # print(token)
    print(
        jwt_handler.decode_jwt(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmUwNDM2ZjktZDBmYS00ZjNkLTg0ZTEtY2M0MzhlMzAyZTkxIiwidXNlcm5hbWUiOiJBcnVsIFMiLCJlbWFpbCI6ImFydWxzYW1wYXRoY3lyQGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwidHlwZSI6ImFjY2Vzc190b2tlbiIsImV4cCI6MTc4MjMwMTAxMH0.PXweIBE2U0UL2Ga0YlBn9ZWvrFsIKnx6-VsQeqHuOMs"
        )
    )
