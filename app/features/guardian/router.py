from datetime import datetime
from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.responses import ORJSONResponse
from fastapi_utils.cbv import cbv
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.dependecies import verify_trainer
from app.core.database import get_db
from app.features.guardian.schemas import GuardianCreate, GuardianRead, GuardianUpdate
from app.features.guardian.service import GuardianService

router = APIRouter(
    prefix="/guardian",
    tags=["guardian"],
    responses={
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[
        Depends(
            # verify_session(),
            get_db,
        )
    ],
)


@cbv(router)
class GuardianRouter:
    # commented for testing
    # session = Depends(verify_trainer())
    service = GuardianService()
    db: Connection = Depends(get_db)

    @router.get(
        "/{guardian_id}",
        response_class=ORJSONResponse,
        response_model=GuardianRead,
    )
    async def read_guardian(
        self,
        guardian_id: UUID1,
    ) -> GuardianRead:
        guardian = await self.service.get_guardian_by_id(guardian_id, self.db)
        return ORJSONResponse(guardian, status_code=200)

    @router.post(
        "/",
        response_class=ORJSONResponse,
        response_model=GuardianRead,
    )
    async def create_guardian(
        self,
        guardian: GuardianCreate,
    ) -> GuardianRead:
        guardian = await self.service.create_guardian(guardian.model_dump(), self.db)
        return ORJSONResponse(guardian, status_code=201)

    async def update_guardian(
        self, guardian_id: UUID1, guardian: GuardianUpdate
    ) -> GuardianRead:
        pass
