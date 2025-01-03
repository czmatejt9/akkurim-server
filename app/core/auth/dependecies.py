from fastapi import Depends
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.exceptions import (
    ClaimValidationError,
    raise_invalid_claims_exception,
)
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.schemas import AuthData


async def verify_and_get_auth_data(
    session: SessionContainer = Depends(verify_session),
) -> AuthData:
    user_roles = await session.get_claim_value(UserRoleClaim)
    if len(user_roles) != 1:
        raise_invalid_claims_exception(
            "Wrong user config", [ClaimValidationError(UserRoleClaim.key, None)]
        )
    user_role = user_roles[0]
    tenant_id, *roles = user_role.split("_")
    return AuthData(tenant_id=tenant_id, roles=roles)


class CheckRoleAndTenant:
    def __init__(self, role: str):
        self.role = role

    async def __call__(
        self, auth_data: AuthData = Depends(verify_and_get_auth_data)
    ) -> AuthData:
        if self.role not in auth_data.roles:
            raise_invalid_claims_exception(
                f"User does not have the required role: {self.role}",
                [ClaimValidationError(UserRoleClaim.key, None)],
            )
        return auth_data


async def is_admin_and_tenant_info(
    auth_data: AuthData = Depends(verify_and_get_auth_data),
) -> AuthData:
    return await CheckRoleAndTenant("admin")(auth_data)


async def is_trainer_and_tenant_info(
    auth_data: AuthData = Depends(verify_and_get_auth_data),
) -> AuthData:
    return await CheckRoleAndTenant("trainer")(auth_data)


tenant_and_roles = Depends(verify_and_get_auth_data)
is_athlete_and_tenant_info = CheckRoleAndTenant("athlete")
is_guardian_and_tenant_info = CheckRoleAndTenant("guardian")
