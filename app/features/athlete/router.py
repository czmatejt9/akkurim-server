from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_utils import cbv
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.database import get_db
from app.features.athlete.schemas import Athlete, AthleteCreate

router = APIRouter(
    prefix="/athlete",
    tags=["athlete"],
    responses={
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(get_db)],
)
SessionType = Annotated[
    SessionContainer,
    Depends(
        verify_session(
            override_global_claim_validators=lambda global_validators, session, user_context: global_validators
            + [UserRoleClaim.validators.includes("trainer")]
        )
    ),
]
