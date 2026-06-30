from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

# Provider Table


class Provider(Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"


class ProviderCreate(BaseModel):
    provider_name: Provider
    user_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)


class ProviderGet(BaseModel):
    provider_name: Provider
    user_id: UUID
    created_at: datetime
    provider_id: UUID


class UserHasProvider(BaseModel):
    user_id: UUID
    provider_name: Provider
