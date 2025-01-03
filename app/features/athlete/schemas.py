from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr

from app.core.base_schema import BaseSchema


class AthleteBase(BaseSchema):
    id: UUID1
    first_name: str
    last_name: str
    street: str
    # use the schema from schema.sql as a reference
    city: str
    zip: str
    email: EmailStr
    phone: str
    ean: str
    notes: str
    athlete_status_id: UUID1


class Athlete(AthleteBase):
    created_at: Optional[AwareDatetime]
    updated_at: AwareDatetime


class AthleteCreate(AthleteBase):
    pass
