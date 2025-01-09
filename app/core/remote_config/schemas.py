from typing import Optional

from pydantic import AwareDatetime

from app.core.base_schema import BaseSchema, generate_example_values


class RemoteConfigBase(BaseSchema):
    id: int
    welcome_message: Optional[str]
    minimum_app_version: str


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
