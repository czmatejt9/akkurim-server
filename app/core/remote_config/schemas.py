from typing import Optional

from pydantic import AwareDatetime

from app.core.shared.base_schema import BaseSchema, generate_example_values


class RemoteConfigBase(BaseSchema):
    id: int
    welcome_message: Optional[str]
    minimum_app_version: str


class RemoteConfigCreate(RemoteConfigBase):
    pass


class RemoteConfigCreatePublic(RemoteConfigCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigCreate),
            ],
        }
    }


class RemoteConfigUpdate(RemoteConfigBase):
    updated_at: AwareDatetime


class RemoteConfigUpdatePublic(RemoteConfigUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigUpdate),
            ],
        }
    }


class RemoteConfigRead(RemoteConfigBase):
    created_at: AwareDatetime
    updated_at: AwareDatetime


class RemoteConfigReadPublic(RemoteConfigRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(RemoteConfigRead),
            ],
        }
    }
