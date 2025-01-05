from datetime import datetime

import orjson
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
from pydantic import UUID1

from app.core.database import get_db
from app.core.exceptions import AlreadyUpdatedError
from app.core.sse.broadcast import broadcast
from app.core.sse.schemas import LocalActionEnum, SSEEvent
from app.core.utils.default_service import DefaultService
from app.features.guardian.schemas import GuardianRead


class GuardianService:
    def __init__(self):
        self.table = "guardian"
        self.default_service = DefaultService(
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
        return await self.default_service.get_object_by_id(
            tenant_id,
            guardian_id,
            db,
        )

    async def create_guardian(
        self,
        tenant_id: str,
        guardian: dict,
        db: Connection,
    ) -> GuardianRead:
        return await self.default_service.create_object(
            tenant_id,
            guardian,
            db,
        )

    async def update_guardian(
        self,
        tenant_id: str,
        guardian: dict,
        db: Connection,
    ) -> GuardianRead:
        return await self.default_service.update_object(
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
        return await self.default_service.delete_object(
            tenant_id,
            guardian_id,
            db,
        )

    async def get_all_guardians(self, tenant_id: str, db: Connection) -> list[dict]:
        return await self.default_service.get_all_objects(tenant_id, db)

    async def get_all_guardians_updated_after(
        self,
        tenant_id: str,
        last_updated: datetime,
        db: Connection,
    ) -> list[dict]:
        return await self.default_service.get_all_objects_updated_after(
            tenant_id,
            last_updated,
            db,
        )
