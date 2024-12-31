from datetime import datetime
from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.database import get_db
from app.features.guardian.schemas import Guardian, GuardianCreate

router = APIRouter(
    prefix="/guardian",
    tags=["guardian"],
    responses={
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[
        Depends(get_db),
        # Depends(verify_session()),
    ],  # TODO: add permission check
)
DBConnection = Annotated[Connection, Depends(get_db)]
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
    "/{guardian_id}",
    response_model=Guardian,
    responses={404: {"description": "Not found"}},
)
async def read_guardian(
    guardian_id: UUID1,
    db: DBConnection,
    # session: SessionType,
):
    guardian = await db.fetchrow(
        """SELECT * FROM guardian WHERE id = $1""", guardian_id
    )
    if not guardian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    guardian = Guardian(**dict(guardian))
    return guardian


@router.put(
    "/{guardian_id}",
    status_code=204,
    responses={409: {"description": "Conflict"}},
)
async def update_guardian(
    guardian_id: UUID1,
    guardian_data: Guardian,
    db: DBConnection,
):
    if guardian_id != guardian_data.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if not await db.fetchrow("""SELECT * FROM guardian WHERE id = $1""", guardian_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.execute(
        """UPDATE guardian SET first_name = $2, last_name = $3, 
        email = $4, phone = $5 updated_at = $6 WHERE id = $1""",
        guardian_data.id,
        guardian_data.first_name,
        guardian_data.last_name,
        guardian_data.email,
        guardian_data.phone,
        guardian_data.updated_at,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{guardian_id}",
    response_model=Guardian,
    status_code=201,
    responses={409: {"description": "Conflict"}},
)
async def create_guardian(
    guardian_id: UUID1,
    guardian_data: GuardianCreate,
    db: DBConnection,
    # session: SessionType,
):
    if guardian_id != guardian_data.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if await db.fetchrow("""SELECT * FROM guardian WHERE id = $1""", guardian_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    await db.execute(
        """INSERT INTO guardian (id, first_name, last_name, email, phone) VALUES ($1, $2, $3, $4, $5)""",
        guardian_id,
        guardian_data.first_name,
        guardian_data.last_name,
        guardian_data.email,
        guardian_data.phone,
    )
    guardian = await db.fetchrow(
        """select * from guardian where id = $1""", guardian_id
    )
    guardian = Guardian(**dict(guardian))
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{guardian_id}",
    status_code=204,
    responses={404: {"description": "Not found"}},
)
async def delete_guardian(
    guardian_id: UUID1,
    db: DBConnection,
):
    if not await db.fetchrow("""SELECT * FROM guardian WHERE id = $1""", guardian_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.execute("""DELETE FROM guardian WHERE id = $1""", guardian_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
