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
    auth_data=Depends(verify_and_get_auth_data),
) -> AuthData:
    return auth_data


@cbv(router)
class GuardianRouter:
    auth_data = Depends(verify_and_get_auth_data)
    db = Annotated[Connection, Depends(get_db)]
    service = GuardianService()

    @router.get(
        "/{guardian_id}",
        response_model=GuardianRead,
    )
    async def read_guardian(
        self,
        guardian_id: UUID1,
    ) -> GuardianRead:
        guardian = await self.service.get_guardian_by_id(
            self.auth_data.tenant_id,
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
        print(type(self.auth_data))
        print(dir(self.auth_data))
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
        self, guardian_id: UUID1, guardian: GuardianUpdate
    ) -> GuardianRead:
        if guardian_id != guardian.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guardian ID in URL and body does not match",
            )
        guardian = await self.service.update_guardian(
            self.auth_data.tenant_id,
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
    ) -> ORJSONResponse:
        await self.service.delete_guardian(
            self.auth_data.tenant_id,
            guardian_id,
            self.db,
        )
        return ORJSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    @router.get(
        "/",
        response_model=list[GuardianRead],
    )
    async def read_all_guardians(self) -> list[dict]:
        guardians = await self.service.get_all_guardians(
            self.auth_data.tenant_id,
            self.db,
        )
        return ORJSONResponse(guardians, status_code=status.HTTP_200_OK)
