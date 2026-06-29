from uuid import UUID

from src.command.commands.authentication import (
    CreateUser,
    EmailVerify,
    GetUserContext,
    ProviderCreate,
    ProviderGet,
    UserContext,
    UserHasProvider,
)
from src.database import DBManager


class AuthenticationRepository:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create_user(self, user: CreateUser) -> UserContext:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                INSERT INTO users (username, password, email, role, created_at, updated_at, email_verified, created_by, updated_by, deleted_by, deleted_at)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id, username, email, role, email_verified;
                """
                cur.execute(
                    query,
                    (
                        user.username,
                        user.password,
                        user.email,
                        user.role.value,
                        user.created_at,
                        user.updated_at,
                        user.email_verified,
                        user.created_by,
                        user.updated_by,
                        user.deleted_by,
                        user.deleted_at,
                    ),
                )

                user_data = cur.fetchone()

            self.db_manager.release_connection(conn)

        return UserContext.model_validate(user_data)

    def get_user_by_id(self, user_id: UUID) -> CreateUser | None:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                SELECT * FROM users WHERE user_id = %s;
                """
                cur.execute(query, (str(user_id),))
                user_data = cur.fetchone()
            self.db_manager.release_connection(conn)

        return CreateUser.model_validate(user_data) if user_data else None

    def get_user_by_email(self, email: str) -> CreateUser | None:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                SELECT * FROM users WHERE email = %s;
                """
                cur.execute(query, (email,))
                user_data = cur.fetchone()
                print(user_data)

            self.db_manager.release_connection(conn)

        return CreateUser.model_validate(user_data) if user_data else None

    def get_user_context(self, cmd: GetUserContext) -> UserContext | None:
        if cmd.user_id is None:
            query = """
            SELECT user_id, username, email, role, email_verified FROM users WHERE email = %s;
            """
            value = (str(cmd.email),)
        else:
            query = """
            SELECT user_id, username, email, role, email_verified FROM users WHERE user_id = %s;
            """
            value = (str(cmd.user_id),)

        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, value)
                user_data = cur.fetchone()
            self.db_manager.release_connection(conn)

        return UserContext.model_validate(user_data) if user_data else None

    def create_provider(self, provider: ProviderCreate) -> ProviderGet | None:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                INSERT INTO providers (user_id, provider_name, created_at)
                VALUES (%s, %s, %s) RETURNING *;
                """
                cur.execute(
                    query,
                    (
                        str(provider.user_id),
                        provider.provider_name.value,
                        provider.created_at,
                    ),
                )

                provider_data = cur.fetchone()
            self.db_manager.release_connection(conn)

        return ProviderGet.model_validate(provider_data) if provider_data else None

    def get_provider(self, cmd: UserHasProvider) -> ProviderGet | None:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                SELECT * FROM providers
                WHERE user_id = %s AND provider_name = %s
                """
                values = (str(cmd.user_id), cmd.provider_name.value)

                cur.execute(sql, values)
                count = cur.fetchone()
            self.db_manager.release_connection(conn)
        return ProviderGet.model_validate(count) if count else None

    # Verify email
    def verify_email(self, cmd: EmailVerify) -> UserContext | None:
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                    UPDATE users
                    SET email_verified = %s
                    WHERE email = %s
                    RETURNING user_id, username, email, role, email_verified
                """
                values = (cmd.email_verified, cmd.email)
                cur.execute(sql, values)
                result = cur.fetchone()
            self.db_manager.release_connection(conn)
        return UserContext.model_validate(result) if result else None


if __name__ == "__main__":
    db = DBManager()
    auth_repo = AuthenticationRepository(db)

    # print(
    #     auth_repo.create_user(
    #         CreateUser(
    #             username="arul",
    #             email="arulsampathcyr@gmail.com",
    #             password="123",
    #             role=Role.STUDENT,
    #         )
    #     )
    # )

    # print(auth_repo.get_user_by_email("arulsampathcyr@gmail.com"))
    # print(auth_repo.get_user_by_id(UUID("f483570e-ffc2-4306-b8aa-204d4784ebd9")))
    # print(auth_repo.get_user_context(GetUserContext(email="arulsampathcyr@gmail.com")))

    #
