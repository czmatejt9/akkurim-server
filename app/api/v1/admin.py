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


@router.post(
    "/add-role",
    status_code=204,
    responses={409: {"description": "Conflict"}},
)
async def add_role(
    session: SessionType,
    role: str,
):
    if "admin" not in session.get_user_info().roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await add_role_to_user(session, role)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
