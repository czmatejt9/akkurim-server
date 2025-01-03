from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr

from app.core.base_schema import BaseSchema


class GuardianBase(BaseSchema):
    id: UUID1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class GuardianCreate(GuardianBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "268f74bc-c7c4-11ef-9cd2-0242ac120002",
                    "first_name": "Pepa",
                    "last_name": "Novák",
                    "email": "pepicek@email.cz",
                    "phone": "00420123456789",
                }
            ]
        }
    }


class GuardianUpdate(GuardianBase):
    updated_at: AwareDatetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "268f74bc-c7c4-11ef-9cd2-0242ac120002",
                    "first_name": "Pepa",
                    "last_name": "Novák",
                    "email": "pepicek@email.cz",
                    "phone": "00420123456789",
                    "updated_at": "2022-04-01T10:00:00+02:00",
                }
            ]
        }
    }


class GuardianRead(GuardianUpdate):
    created_at: AwareDatetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "268f74bc-c7c4-11ef-9cd2-0242ac120002",
                    "first_name": "Pepa",
                    "last_name": "Novák",
                    "email": "pepicek@email.cz",
                    "phone": "00420123456789",
                    "created_at": "2022-04-01T10:00:00+02:00",
                    "updated_at": "2022-04-01T10:00:00+02:00",
                }
            ]
        }
    }
