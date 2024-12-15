from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.db.database import get_db
from app.schemas.athlete import Athlete, AthleteCreate

router = APIRouter(
    prefix="/v1/athlete",
    tags=["athlete"],
    responses={
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(get_db())],
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


@router.get(
    "/{athlete_id}",
    response_model=Athlete,
    responses={404: {"description": "Not found"}},
)
async def read_athlete(athlete_id: UUID1, db: Connection):
    athlete = await db.fetchrow("""SELECT * FROM athlete WHERE id = $1""", athlete_id)
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    athlete = Athlete(**dict(athlete))
    return athlete
