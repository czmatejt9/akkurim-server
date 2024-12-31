from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr

from app.core.base_schema import CustomBaseModel


class GuardianBase(CustomBaseModel):
    id: UUID1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

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


class GuardianCreate(GuardianBase):
    pass


class GuardianUpdate(GuardianBase):
    updated_at: AwareDatetime


class GuardianRead(GuardianUpdate):
    created_at: Optional[AwareDatetime]
