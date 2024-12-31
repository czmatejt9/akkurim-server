from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.remote_config.schemas import RemoteConfig

router = APIRouter(
    prefix="/remote-config",
    tags=["remote-config"],
    responses={},
    dependencies=[
        Depends(get_db),
    ],
)
DBConection = Annotated[Connection, Depends(get_db)]


@router.get(
    "/{remote_config_id}",
    status_code=status.HTTP_200_OK,
    response_model=RemoteConfig,
    responses={404: {"description": "Not found"}},
)
async def read_remote_config(remote_config_id: int, db: DBConection):
    remote_config = await db.fetchrow(
        """SELECT * FROM remote_config WHERE id = $1""", remote_config_id
    )
    if not remote_config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    remote_config = RemoteConfig(**dict(remote_config))
    return remote_config
