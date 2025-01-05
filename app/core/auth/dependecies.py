from fastapi import Depends
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.exceptions import (
    ClaimValidationError,
    raise_invalid_claims_exception,
)
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.schemas import AuthData
from app.core.config import settings


async def verify_and_get_auth_data(
    session: SessionContainer = Depends(verify_session()),
) -> AuthData:
    user_roles = await session.get_claim_value(UserRoleClaim)
    if len(user_roles) != 1:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    user_role: str = user_roles[0]
    tenant_id, *roles = user_role.split("_")
    return AuthData(tenant_id=tenant_id, roles=roles)


def fake_auth_data():
    user_role = "akkurim_trainer"
    tenant_id, *roles = user_role.split("_")
    return AuthData(tenant_id=tenant_id, roles=roles)


async def is_trainer_and_tenant_info(
    auth_data: AuthData = (
        Depends(verify_and_get_auth_data)
        if not settings.DEBUG
        else Depends(fake_auth_data)
    ),
) -> AuthData:
    if "trainer" not in auth_data.roles:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    return auth_data
