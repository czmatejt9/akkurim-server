from typing import Optional

from pydantic import AwareDatetime, BaseModel

from app.core.base_schema import CustomBaseModel


class RemoteConfigBase(CustomBaseModel):
    id: int
    server_url: str
    websocket_url: str
    dev_prefix: str
    welcome_message: Optional[str]
    minimum_app_version: str


class RemoteConfig(RemoteConfigBase):
    created_at: Optional[AwareDatetime]
    updated_at: AwareDatetime
