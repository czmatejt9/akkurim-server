from typing import Annotated, Optional

from pydantic import UUID1, AfterValidator, AwareDatetime, EmailStr, Field

from app.core.base_schema import BaseSchema
from app.features.athlete.utils import validate_birth_number


class AthleteBase(BaseSchema):
    id: UUID1
    birth_number: Annotated[str, AfterValidator(validate_birth_number)]
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


class AthleteUpdate(AthleteBase):
    updated_at: AwareDatetime


class AthleteRead(AthleteUpdate):
    created_at: AwareDatetime
