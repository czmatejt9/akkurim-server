from datetime import datetime
from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.responses import ORJSONResponse
from fastapi_utils.cbv import cbv
from pydantic import UUID1
from supertokens_python.recipe.session.framework.fastapi import verify_session

from app.core.auth.dependecies import (
    is_trainer_and_tenant_info,
    verify_and_get_auth_data,
)
from app.core.auth.schemas import AuthData
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
        Depends(get_db),
    ],
    default_response_class=ORJSONResponse,
)


@router.get(
    "test",
    response_model=AuthData,
)
async def test(
    auth_data=Depends(is_trainer_and_tenant_info),
) -> dict:
    return ORJSONResponse(
        {"message": auth_data.tenant_id}, status_code=status.HTTP_200_OK
    )


@cbv(router)
class GuardianRouter:
    db = get_db()
    service = GuardianService()
    auth_data = is_trainer_and_tenant_info()

    @router.get(
        "/{guardian_id}",
        response_model=GuardianRead,
    )
    async def read_guardian(
        self,
        guardian_id: UUID1,
        auth_data=Depends(is_trainer_and_tenant_info),
    ) -> GuardianRead:
        guardian = await self.service.get_guardian_by_id(
            auth_data.tenant_id,
            guardian_id,
            self.db,
        )
        return ORJSONResponse(guardian, status_code=status.HTTP_200_OK)

    @router.post(
        "/",
        response_model=GuardianRead,
    )
    async def create_guardian(
        self,
        guardian: GuardianCreate,
    ) -> GuardianRead:
        guardian = await self.service.create_guardian(
            self.auth_data.tenant_id,
            guardian.model_dump(),
            self.db,
        )
        return ORJSONResponse(guardian, status_code=status.HTTP_201_CREATED)

    @router.put(
        "/{guardian_id}",
        response_model=GuardianRead,
    )
    async def update_guardian(
        self,
        guardian_id: UUID1,
        guardian: GuardianUpdate,
        auth_data=Depends(is_trainer_and_tenant_info),
    ) -> GuardianRead:
        if guardian_id != guardian.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guardian ID in URL and body does not match",
            )
        guardian = await self.service.update_guardian(
            auth_data.tenant_id,
            guardian.model_dump(),
            self.db,
        )
        return ORJSONResponse(guardian, status_code=status.HTTP_200_OK)

    @router.delete(
        "/{guardian_id}",
        status_code=204,
        response_model=None,
    )
    async def delete_guardian(
        self,
        guardian_id: UUID1,
        auth_data=Depends(is_trainer_and_tenant_info),
    ) -> ORJSONResponse:
        await self.service.delete_guardian(
            auth_data.tenant_id,
            guardian_id,
            self.db,
        )
        return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    @router.get(
        "/",
        response_model=list[GuardianRead],
    )
    async def read_all_guardians(
        self,
        auth_data=Depends(is_trainer_and_tenant_info),
    ) -> list[dict]:
        guardians = await self.service.get_all_guardians(
            auth_data.tenant_id,
            self.db,
        )
        return ORJSONResponse(guardians, status_code=status.HTTP_200_OK)

    # todo probably move the updated_at to query params
    @router.get(
        "/sync/{last_updated_at}",
        response_model=list[GuardianRead],
    )
    async def read_all_guardians_updated_after(
        self,
        last_updated_at: Annotated[datetime, Path(...)],
        auth_data=Depends(is_trainer_and_tenant_info),
    ) -> list[dict]:
        guardians = await self.service.get_all_guardians_updated_after(
            auth_data.tenant_id,
            last_updated_at,
            self.db,
        )
        return ORJSONResponse(guardians, status_code=status.HTTP_200_OK)
