from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles.asyncio import (
    add_role_to_user,
    create_new_role_or_add_permissions,
)

router = APIRouter(
    prefix="v1/admin",
    tags=["admin"],
    responses={
        "401": {"description": "Unauthorized"},
        "403": {"description": "Forbidden"},
    },
    dependencies=[Depends(verify_session())],
)
SessionType = Annotated[SessionContainer, Depends(verify_session())]


# only a one time setup to create the admin role TODO change it to add any role
@router.get(
    "/create-role",
    status_code=204,
    responses={201: {"description": "Created"}},
)
async def create_role(
    session: SessionType,
):
    try:
        await create_new_role_or_add_permissions("admin", ["read", "write"])
        await add_role_to_user(
            "public", "d81fbff7-ea4e-4fc4-8df3-f9b06619f0ea", "admin"
        )
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
