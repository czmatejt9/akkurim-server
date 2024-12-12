from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.db.database import get_db
from app.schemas.guardian import Guardian, GuardianCreate

router = APIRouter(
    prefix="/v1/guardian",
    tags=["guardian"],
    responses={
        "401": {"description": "Unauthorized"},
        "400": {"description": "Bad Request"},
    },
    dependencies=[get_db, verify_session],  # TODO: add permission check
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
    session: SessionType,
):
    guardian = await db.fetchrow(
        """SELECT * FROM guardian WHERE id = $1""", guardian_id
    )
    if not guardian:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
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
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


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

    db.execute(
        """INSERT INTO guardian (id, first_name, last_name, email, phone) VALUES ($1, $2, $3, $4, $5)""",
        guardian_id,
        guardian_data.first_name,
        guardian_data.last_name,
        guardian_data.email,
        guardian_data.phone,
    )
    guardian = await db.fetchrow(
        """SELECT * FROM guardian WHERE id = $1""", guardian_id
    )

    return Response(guardian, status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{guardian_id}",
    status_code=204,
    responses={404: {"description": "Not found"}},
)
async def delete_guardian(
    guardian_id: UUID1,
    db: DBConnection,
):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get(
    "/page/{page_number}",
    response_model=list[Guardian],
)
async def read_guardians(
    page_number: Annotated[
        int,
        Path(
            ...,
            title="Page number",
            description="0 for all, 1 for 1-10, 2 for 11-20 etc.",
            ge=0,
        ),
    ],
    db: DBConnection,
):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get(
    "/search/",
    response_model=list[Guardian],
    status_code=501,
)
async def search_guardians(
    query: str,
    db: DBConnection,
):
    # TODO: implement full text search
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)
