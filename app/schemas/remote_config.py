from typing import Optional

from pydantic import AwareDatetime, BaseModel


class RemoteConfigBase(BaseModel):
    id: int
    server_url: str
    web_socket_url: str
    dev_prefix: str
    welcome_message: Optional[str]
    minimum_app_version: str


class RemoteConfig(RemoteConfigBase):
    created_at: Optional[AwareDatetime]
    updated_at: AwareDatetime
