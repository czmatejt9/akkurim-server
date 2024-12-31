from datetime import datetime

from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
from fastapi import Depends
from pydantic import UUID1

from app.core.database import get_db
from app.core.utils import (
    generate_sql_insert,
    generate_sql_insert_with_returning,
    generate_sql_read,
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

    async def _get_guardian_by_id(
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
        guardian = await self._get_guardian_by_id(guardian_id, db)
        if not guardian:
            raise GuardianNotFoundException
        return dict(guardian)

    async def create_guardian(self, guardian: dict, db: Connection) -> GuardianRead:
        exists = await self._get_guardian_by_id(guardian["id"], db)
        if exists:
            raise GuardianAlreadyExistsException

        try:
            query, values = generate_sql_insert_with_returning(
                self.table,
                guardian,
                GuardianRead.model_fields.keys(),
            )
            created = await db.fetchrow(query, *values)
            return dict(created)
        except UniqueViolationError:
            raise GuardianEmailAlreadyExistsException
