from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1, AwareDatetime

from app.core.auth.dependecies import (
    is_admin_and_tenant_info,
    is_trainer_and_tenant_info,
    verify_and_get_auth_data,
)
from app.core.auth.schemas import AuthData
from app.core.shared.database import get_db
from app.core.shared.schemas import SchoolYearCreate, SchoolYearRead
from app.core.shared.service import SchoolYearService

router = APIRouter(
    prefix="/",
    tags=["shared"],
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
    ],
    default_response_class=ORJSONResponse,
)

admin_dep = Annotated[AuthData, Depends(is_admin_and_tenant_info)]
db_dep = Annotated[Connection, Depends(get_db)]
service_dep = Annotated[SchoolYearService, Depends(SchoolYearService)]
trainer_dep = Annotated[AuthData, Depends(is_trainer_and_tenant_info)]
auth_data_dep = Annotated[AuthData, Depends(verify_and_get_auth_data)]


@router.post(
    "/school_year",
    response_model=SchoolYearRead,
)
async def create_school_year(
    school_year: SchoolYearCreate,
    auth_data: admin_dep,
    db: db_dep,
    service: service_dep,
) -> SchoolYearRead:
    return await service.create_school_year(
        auth_data.tenant_id,
        school_year,
        db,
    )


@router.get(
    "/school_year/{school_year_id}",
    response_model=SchoolYearRead,
)
async def read_school_year(
    school_year_id: UUID1,
    auth_data: auth_data_dep,
    db: db_dep,
    service: service_dep,
) -> SchoolYearRead:
    return await service.get_school_year_by_id(
        auth_data.tenant_id,
        school_year_id,
        db,
    )


@router.get(
    "/school_year/",
    response_model=list[SchoolYearRead],
)
async def read_all_school_years(
    auth_data: auth_data_dep,
    db: db_dep,
    service: service_dep,
) -> list[SchoolYearRead]:
    return await service.get_all_school_years(
        auth_data.tenant_id,
        db,
    )
