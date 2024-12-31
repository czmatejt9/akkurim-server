from asyncpg import Connection
from fastapi import Depends
from pydantic import UUID1

from app.core.database import get_db
from app.core.utils import generate_sql_read
from app.features.guardian.exceptions import GuardianNotFoundException
from app.features.guardian.schemas import GuardianRead


class GuardianService:
    def __init__(self, db: Connection = Depends(get_db())) -> None:
        self.db = db
        self.table = "guardian"

    async def get_guardian_by_id(self, guardian_id: UUID1) -> GuardianRead:
        query, values = generate_sql_read(
            self.table,
            ["*"],
            {"id": guardian_id},
        )
        guardian = await self.db.fetchrow(query, *values)
        if not guardian:
            raise GuardianNotFoundException
        return GuardianRead(**dict(guardian))
