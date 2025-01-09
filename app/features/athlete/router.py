from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

from app.core.auth.dependecies import is_trainer_and_tenant_info
from app.core.auth.schemas import AuthData
from app.core.database import get_db
from app.features.athlete.schemas import AthleteCreate, AthleteRead, AthleteUpdate
from app.features.athlete.service import AthleteService

router = APIRouter(
    prefix="/athlete",
    tags=["athlete"],
    responses={
        "200": {"description": "Success"},
        "400": {"description": "Bad Request"},
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
        "404": {"description": "Not Found"},
        "409": {"description": "Conflict"},
    },
    dependencies=[
        Depends(get_db),
        Depends(AthleteService),
    ],
    default_response_class=ORJSONResponse,
)

trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[AthleteService, Depends(AthleteService)]


@router.get(
    "/{athlete_id}",
    response_model=AthleteRead,
)
async def read_athlete(
    athlete_id: UUID1,
    auth_data: trainer_dep,
    db: db_dep,
    service: service_dep,
) -> AthleteRead:
    athlete = await service.get_athlete_by_id(
        auth_data.tenant_id,
        athlete_id,
        db,
    )
    return ORJSONResponse(athlete, status_code=status.HTTP_200_OK)
