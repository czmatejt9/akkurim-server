from typing import Annotated, Optional

from pydantic import UUID1, AfterValidator, AwareDatetime, EmailStr

from app.core.base_schema import BaseSchema, generate_example_values
from app.features.athlete.utils import pydanyic_validate_birth_number


class AthleteBase(BaseSchema):
    id: UUID1
    birth_number: Annotated[str, AfterValidator(pydanyic_validate_birth_number)]
    first_name: str
    last_name: str
    street: str
    city: str
    zip: str
    email: Optional[EmailStr]
    phone: Optional[str]
    ean: Optional[str]
    note: Optional[str]
    club_id: str
    profile_picture: Optional[str]
    athlete_status_id: UUID1


class AthleteCreate(AthleteBase):
    pass


class AthleteCreatePublic(AthleteCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteCreate),
            ],
        }
    }


class AthleteUpdate(AthleteBase):
    updated_at: AwareDatetime


class AthleteUpdatePublic(AthleteUpdate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteUpdate),
            ],
        }
    }


class AthleteRead(AthleteBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class AthleteReadPublic(AthleteRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteRead),
            ],
        }
    }


class AthleteStatusBase(BaseSchema):
    id: UUID1
    name: str
    description: Optional[str]


class AthleteStatusRead(AthleteStatusBase):
    updated_at: AwareDatetime
    created_at: AwareDatetime


class AthleteStatusReadPublic(AthleteStatusRead):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteStatusRead),
            ],
        }
    }


class AthleteStatusCreate(AthleteStatusBase):
    pass


class AthleteStatusCreatePublic(AthleteStatusCreate):
    model_config = {
        "json_schema_extra": {
            "examples": [
                generate_example_values(AthleteStatusCreate),
            ],
        }
    }
