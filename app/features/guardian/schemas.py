from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr

from app.core.base_schema import MyBase


class GuardianBase(MyBase):
    id: UUID1
    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class GuardianCreate(GuardianBase):
    pass


class GuardinaUpdate(GuardianBase):
    updated_at: AwareDatetime


class GuardianRead(GuardinaUpdate):
    created_at: Optional[AwareDatetime]
