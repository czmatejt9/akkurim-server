from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim


def verify_trainer():
    return verify_session(
        override_global_claim_validators=lambda global_validators,
        session,
        user_context: global_validators + [UserRoleClaim.validators.includes("trainer")]
    )
