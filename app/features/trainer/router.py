from typing import Annotated

from asyncpg import Connection
from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID1, AwareDatetime

from app.core.auth.dependecies import (
    is_admin_and_tenant_info,
    is_trainer_and_tenant_info,
)
from app.core.auth.schemas import AuthData
from app.core.shared.database import get_db
from app.features.trainer.schemas import TrainerReadPublic
from app.features.trainer.service import TrainerService

router = APIRouter(
    prefix="/trainer",
    tags=["trainer"],
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
        Depends(TrainerService),
    ],
    default_response_class=ORJSONResponse,
)
