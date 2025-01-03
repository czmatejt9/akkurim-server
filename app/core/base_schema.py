from typing import Any

from pydantic import UUID1, BaseModel, EmailStr


# used for global configuration
class BaseSchema(BaseModel):
    pass
