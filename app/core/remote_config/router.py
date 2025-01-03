from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi_utils.cbv import cbv

from app.core.database import get_db
from app.core.remote_config.schemas import RemoteConfigRead
from app.core.remote_config.service import RemoteConfigService

router = APIRouter(
    prefix="/remote-config",
    tags=["remote-config"],
    responses={},
    dependencies=[
        Depends(get_db),
    ],
    default_response_class=ORJSONResponse,
)


@cbv(router)
class RemoteConfigRouter:
    db = Depends(get_db)
    service = RemoteConfigService()

    @router.get(
        "/",
        response_model=RemoteConfigRead,
    )
    async def get_remote_config(
        self,
    ) -> RemoteConfigRead:
        remote_config = await self.service.get_remote_config("public", self.db)
        return ORJSONResponse(remote_config, status_code=200)
