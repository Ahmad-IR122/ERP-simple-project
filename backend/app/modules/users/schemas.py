from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    clerk_user_id: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=1, max_length=320)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    role: str = Field(default="employee", min_length=1, max_length=100)


class UserUpdate(BaseModel):
    clerk_user_id: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, min_length=1, max_length=320)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    role: str | None = Field(default=None, min_length=1, max_length=100)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    clerk_user_id: str
    email: str
    first_name: str | None
    last_name: str | None
    role: str
    created_at: datetime
    updated_at: datetime
