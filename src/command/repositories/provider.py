from src.command.commands.provider import (
    ProviderCreate,
    ProviderGet,
    UserHasProvider,
)
from src.database import DBManager


class ProviderRepository:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create(self, provider: ProviderCreate) -> ProviderGet | None:
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

    def get(self, cmd: UserHasProvider) -> ProviderGet | None:
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
