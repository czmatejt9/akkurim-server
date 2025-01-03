from typing import Optional

from pydantic import AwareDatetime

from app.core.base_schema import BaseSchema


class RemoteConfigBase(BaseSchema):
    id: int
    welcome_message: Optional[str]
    minimum_app_version: str


class RemoteConfigRead(RemoteConfigBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime
