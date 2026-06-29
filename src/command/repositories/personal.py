import datetime
import uuid

from src.command.commands.personal import (
    AddressInfo,
    ContactInfo,
    Create,
    PersonalInfo,
    Update,
)
from src.database import DBManager


class PersonalRepository:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def create(self, cmd: Create):
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO personal_details (
                    user_id,
                    date_of_birth,
                    gender,
                    nationality,
                    phone_number,
                    alternate_phone_number,
                    street,
                    city,
                    district,
                    state,
                    pin_code,
                    country,
                    created_by
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING *;
                """
                values = (
                    str(cmd.user_id),
                    str(cmd.personal_info.date_of_birth),
                    cmd.personal_info.gender,
                    cmd.personal_info.nationality,
                    cmd.contact_info.phone_number,
                    cmd.contact_info.alternate_phone_number,
                    cmd.address_info.street,
                    cmd.address_info.city,
                    cmd.address_info.district,
                    cmd.address_info.state,
                    cmd.address_info.pin_code,
                    cmd.address_info.country,
                    str(cmd.created_by),
                )
                cur.execute(sql, values)
                result = cur.fetchone()

            self.db_manager.release_connection(conn)

        return result  # type: ignore

    def update(self, cmd: Update):
        with self.db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                if cmd.personal_info:
                    sql = """
                    UPDATE personal_details
                    SET
                        date_of_birth = %s,
                        gender = %s,
                        nationality = %s
                    WHERE user_id = %s
                    """
                    values = (
                        cmd.personal_info.date_of_birth,
                        cmd.personal_info.gender,
                        cmd.personal_info.nationality,
                        str(cmd.user_id),
                    )
                    cur.execute(sql, values)
                if cmd.contact_info:
                    sql = """
                    UPDATE contact_info
                    SET
                        phone_number = %s,
                        alternate_phone_number = %s
                    WHERE user_id = %s
                    """
                    values = (
                        cmd.contact_info.phone_number,
                        cmd.contact_info.alternate_phone_number,
                        str(cmd.user_id),
                    )
                    cur.execute(sql, values)
                if cmd.address_info:
                    sql = """
                    UPDATE address_info
                    SET
                        street = %s,
                        city = %s,
                        district = %s,
                        state = %s,
                        pin_code = %s,
                        country = %s
                    WHERE user_id = %s
                    """
                    values = (
                        cmd.address_info.street,
                        cmd.address_info.city,
                        cmd.address_info.district,
                        cmd.address_info.state,
                        cmd.address_info.pin_code,
                        cmd.address_info.country,
                        str(cmd.user_id),
                    )
                    cur.execute(sql, values)

                sql = """
                UPDATE personal_info
                SET
                    updated_by = %s,
                    updated_at = NOW(),
                WHERE user_id = %s
                """
                values = (
                    str(cmd.updated_by),
                    str(cmd.user_id),
                )
                cur.execute(sql, values)

            self.db_manager.release_connection(conn)

        return None


if __name__ == "__main__":
    db_manager = DBManager()
    repo = PersonalRepository(db_manager)

    personal_info = PersonalInfo(
        date_of_birth=datetime.date.today(),
        gender="Male",
        nationality="Indian",
    )
    contact_info = ContactInfo(
        phone_number="9876543210",
        alternate_phone_number="9876543210",
    )
    address_info = AddressInfo(
        street="123, Main Street",
        city="Chennai",
        district="Chennai",
        state="Tamil Nadu",
        pin_code="600001",
        country="India",
    )
    cmd = Create(
        user_id=uuid.uuid4(),
        created_by=uuid.uuid4(),
        personal_info=personal_info,
        contact_info=contact_info,
        address_info=address_info,
    )
    result = repo.create(cmd=cmd)
    print(result)
