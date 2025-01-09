from datetime import datetime

from asyncpg import Connection
from pydantic import UUID1

from app.core.utils.default_service import DefaultService
from app.features.guardian.schemas import GuardianCreate, GuardianRead, GuardianUpdate


class GuardianService(DefaultService):
    def __init__(self):
        super().__init__(
            "guardian",
            "/guardian/{id}",
            GuardianRead,
        )

    async def get_guardian_by_id(
        self,
        tenant_id: str,
        guardian_id: UUID1,
        db: Connection,
    ) -> GuardianRead:
        return await super().get_object_by_id(
            tenant_id,
            guardian_id,
            db,
        )

    async def create_guardian(
        self,
        tenant_id: str,
        guardian: GuardianCreate,
        db: Connection,
    ) -> GuardianRead:
        return await super().create_object(
            tenant_id,
            guardian,
            db,
        )

    async def update_guardian(
        self,
        tenant_id: str,
        guardian: GuardianUpdate,
        db: Connection,
    ) -> GuardianRead:
        return await super().update_object(
            tenant_id,
            guardian,
            db,
        )

    async def delete_guardian(
        self,
        tenant_id: str,
        guardian_id: UUID1,
        db: Connection,
    ) -> None:
        return await super().delete_object(
            tenant_id,
            guardian_id,
            db,
        )

    async def get_all_guardians(
        self, tenant_id: str, db: Connection
    ) -> list[GuardianRead]:
        return await super().get_all_objects(tenant_id, db)

    async def get_all_guardians_updated_after(
        self,
        tenant_id: str,
        last_updated: datetime,
        db: Connection,
    ) -> list[GuardianRead]:
        return await super().get_all_objects_updated_after(
            tenant_id,
            last_updated,
            db,
        )
