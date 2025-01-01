from datetime import datetime

from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends
from pydantic import UUID1

from app.core.database import get_db
from app.core.exceptions import UpdateError
from app.core.sse.broadcast import broadcast
from app.core.sse.schemas import LocalActionEnum, SSEEvent
from app.core.utils import (
    convert_uuid_to_str,
    generate_sql_delete_with_returning,
    generate_sql_insert,
    generate_sql_insert_with_returning,
    generate_sql_read,
    generate_sql_update,
    generate_sql_update_with_returning,
)
from app.features.guardian.exceptions import (
    GuardianAlreadyExistsException,
    GuardianEmailAlreadyExistsException,
    GuardianNotFoundException,
)
from app.features.guardian.schemas import GuardianRead


class GuardianService:
    def __init__(self) -> None:
        self.table = "guardian"
        self.broadcast = broadcast

    async def notify_update(self, guardian_id: UUID1) -> None:
        event = SSEEvent(
            table_name=self.table,
            endpoint="/guardian/{id}",
            id=guardian_id,
            local_action=LocalActionEnum.upsert,
        )
        await self.broadcast.publish(
            channel="updates",
            message=event.model_dump(),
        )

    async def notify_delete(self, guardian_id: UUID1) -> None:
        event = SSEEvent(
            table_name=self.table,
            endpoint=None,
            id=guardian_id,
            local_action=LocalActionEnum.delete,
        )
        await self.broadcast.publish(
            channel="updates",
            message=event.model_dump(),
        )

    async def valid_guardian_by_id(
        self,
        guardian_id: UUID1,
        db: Connection,
    ) -> dict | None:
        query, values = generate_sql_read(
            self.table,
            ["*"],
            {"id": guardian_id},
        )
        guardian = await db.fetchrow(query, *values)
        if not guardian:
            return None
        return dict(guardian)

    async def get_guardian_by_id(
        self, guardian_id: UUID1, db: Connection
    ) -> GuardianRead:
        guardian = await self.valid_guardian_by_id(guardian_id, db)
        if not guardian:
            raise GuardianNotFoundException

        return convert_uuid_to_str(guardian)

    async def create_guardian(self, guardian: dict, db: Connection) -> GuardianRead:
        exists = await self.valid_guardian_by_id(guardian["id"], db)
        if exists:
            raise GuardianAlreadyExistsException

        query, values = generate_sql_insert_with_returning(
            self.table,
            guardian,
            GuardianRead.model_fields.keys(),
        )
        try:
            created = await db.fetchrow(query, *values)
            self.notify_update(guardian["id"])
            return convert_uuid_to_str(dict(created))

        except UniqueViolationError:
            raise GuardianEmailAlreadyExistsException

    async def update_guardian(self, guardian: dict, db: Connection) -> GuardianRead:
        exists = await self.valid_guardian_by_id(guardian["id"], db)
        if not exists:
            raise GuardianNotFoundException

        if exists["updated_at"] > guardian["updated_at"]:
            raise UpdateError

        guardian["updated_at"] = datetime.now()
        query, values = generate_sql_update_with_returning(
            self.table,
            guardian,
            {"id": guardian["id"]},
            GuardianRead.model_fields.keys(),
        )
        print(query, values)
        try:
            updated = await db.fetchrow(query, *values)
            self.notify_update(guardian["id"])
            return convert_uuid_to_str(dict(updated))
        except UniqueViolationError:
            raise GuardianEmailAlreadyExistsException

    async def delete_guardian(self, guardian_id: UUID1, db: Connection) -> None:
        exists = await self.valid_guardian_by_id(guardian_id, db)
        if not exists:
            raise GuardianNotFoundException

        query, values = generate_sql_delete_with_returning(
            self.table,
            {"id": guardian_id},
        )
        result = await db.fetchrow(query, *values)
        if not result:
            raise GuardianNotFoundException
        self.notify_delete(guardian_id)
        return None
