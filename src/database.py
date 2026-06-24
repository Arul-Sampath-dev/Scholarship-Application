from typing import Optional

from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from src.settings import settings


class DBManager:
    def __init__(self) -> None:
        self.pool: Optional[SimpleConnectionPool] = None

    def initialize_pool(self) -> None:
        if self.pool is None:
            self.pool = SimpleConnectionPool(
                minconn=settings.database.min_conn,
                maxconn=settings.database.max_conn,
                user=settings.database.user,
                password=settings.database.password,
                host=settings.database.host,
                port=settings.database.port,
                database=settings.database.name,
                cursor_factory=RealDictCursor,
            )

    def close_pool(self) -> None:
        if self.pool is not None:
            self.pool.closeall()

    def get_connection(self) -> connection:
        if self.pool is None:
            self.initialize_pool()
        return self.pool.getconn()  # type: ignore[return-value]

    def release_connection(self, conn: connection) -> None:
        if self.pool is not None:
            self.pool.putconn(conn)
