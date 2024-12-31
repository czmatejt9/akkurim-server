from datetime import datetime
from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi_utils.cbv import cbv
from pydantic import UUID1
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.dependecies import verify_trainer
from app.core.database import get_db
from app.core.json_response import JSONResponse
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
)


@cbv(router)
class GuardianRouter:
    # commented for testing
    # session: SessionContainer = Depends(verify_trainer())
    service: GuardianService = GuardianService()

    @router.get(
        "/{guardian_id}",
        response_model=GuardianRead,
        response_class=JSONResponse,
    )
    async def read_guardian(
        self, guardian_id: UUID1 = Path(..., title="The ID of the guardian to read")
    ):
        return await self.service.get_guardian_by_id(guardian_id)
