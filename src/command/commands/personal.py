from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PersonalInfo(BaseModel):
    date_of_birth: date
    gender: str
    nationality: str


class ContactInfo(BaseModel):
    phone_number: str
    alternate_phone_number: Optional[str] = None


class AddressInfo(BaseModel):
    street: str
    city: str
    district: str
    state: str
    pin_code: str
    country: str


class Create(BaseModel):
    user_id: UUID
    created_by: UUID

    personal_info: PersonalInfo
    contact_info: ContactInfo
    address_info: AddressInfo


class Update(BaseModel):
    user_id: UUID
    updated_by: UUID

    personal_info: Optional[PersonalInfo] = None
    contact_info: Optional[ContactInfo] = None
    address_info: Optional[AddressInfo] = None


class Delete(BaseModel):
    user_id: UUID
    deleted_by: UUID
