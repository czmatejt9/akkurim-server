from typing import Optional

from pydantic import UUID1, AwareDatetime, EmailStr, Field

from app.core.base_schema import MyBase


class GuardianBase(MyBase):
    id: UUID1 = Field(
        ..., json_schema_extra={"example": "91ed85cc-830a-11ef-b864-0242ac120002"}
    )
    first_name: str = Field(..., json_schema_extra={"example": "John"})
    last_name: str = Field(..., json_schema_extra={"example": "Doe"})
    email: EmailStr = Field(..., json_schema_extra={"example": "johndoe@gmail.com"})
    phone: str = Field(..., json_schema_extra={"example": "00420123456789"})


class Guardian(GuardianBase):
    created_at: Optional[AwareDatetime] = Field(
        ..., json_schema_extra={"example": "2022-01-01 00:00:00+01:00"}
    )
    updated_at: AwareDatetime = Field(
        ..., json_schema_extra={"example": "2022-01-01 00:00:00+01:00"}
    )


class GuardianCreate(GuardianBase):
    pass
