from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from pydantic import UUID1

from app.db.database import get_db
from app.schemas.guardian import Guardian, GuardianCreate

router = APIRouter(
    prefix="/v1/guardian",
    tags=["guardian"],
    responses={
        "401": {"description": "Unauthorized"},
        "400": {"description": "Bad Request"},
    },
    dependencies=[],  # TODO: add permission check
)
DBConnection = Annotated[Connection, Depends(get_db)]


@router.get(
    "/{guardian_id}",
    response_model=Guardian,
    responses={404: {"description": "Not found"}},
)
async def read_guardian(
    guardian_id: UUID1,
    db: DBConnection,
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
):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


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
