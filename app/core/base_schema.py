from datetime import datetime
from typing import Any

from pydantic import UUID1, AwareDatetime, BaseModel, EmailStr


# used for global configuration
class BaseSchema(BaseModel):
    pass


def generate_example_values(schema: BaseSchema) -> dict[str, Any]:
    example_values = {}
    for field_name, info in schema.model_fields.items():
        if info.annotation == UUID1:
            example_values[field_name] = "268f74bc-c7c4-11ef-9cd2-0242ac120002"
        elif info.annotation == EmailStr:
            example_values[field_name] = "pepicke@email.cz"
        elif info.annotation == AwareDatetime:
            example_values[field_name] = datetime.now(tz="Europe/Prague").isoformat()
        else:
            if "first_name" in field_name:
                example_values[field_name] = "Pepa"
            elif "last_name" in field_name:
                example_values[field_name] = "Novák"
            elif "street" in field_name:
                example_values[field_name] = "Ulice 9"
            elif "city" in field_name:
                example_values[field_name] = "Praha"
            elif "zip" in field_name:
                example_values[field_name] = "11000"
            elif "phone" in field_name:
                example_values[field_name] = "00420123456789"
            elif "note" in field_name:
                example_values[field_name] = "Poznámka"
            else:
                example_values[field_name] = "some value"

    return example_values
