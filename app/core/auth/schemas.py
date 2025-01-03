from app.core.base_schema import BaseSchema


class AuthData(BaseSchema):
    tenant_id: str
    roles: tuple[str]