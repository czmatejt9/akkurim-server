from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.db.database import get_db
from app.schemas.remote_config import RemoteConfig

router = APIRouter(
    prefix="/v1/remote-config",
    tags=["remote-config"],
    responses={
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(get_db())],
)
DBConection = Annotated[Connection, Depends(get_db)]


@router.get(
    "/{remote_config_id}",
    response_model=RemoteConfig,
    responses={404: {"description": "Not found"}},
)
async def read_remote_config(remote_config_id: int, db: DBConection):
    remote_config = await db.fetchrow
    ("""SELECT * FROM remote_config WHERE id = $1""", remote_config_id)
    if not remote_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    remote_config = RemoteConfig(**dict(remote_config))
    return remote_config
