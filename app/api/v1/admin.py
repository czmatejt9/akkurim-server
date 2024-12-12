from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles.asyncio import (
    add_role_to_user,
    create_new_role_or_add_permissions,
)

router = APIRouter(
    prefix="/v1/admin",
    tags=["admin"],
    responses={
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(verify_session())],
)
SessionType = Annotated[SessionContainer, Depends(verify_session())]
