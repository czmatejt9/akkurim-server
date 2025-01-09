from datetime import datetime

from asyncpg import Connection
from pydantic import UUID1

from app.core.utils.default_service import DefaultService
from app.features.athlete.schemas import AthleteCreate, AthleteRead, AthleteUpdate


class AthleteService(DefaultService):
    def __init__(self):
        super().__init__(
            "athlete",
            "/athlete/{id}",
            AthleteRead,
        )

    async def get_athlete_by_id(
        self,
        tenant_id: str,
        athlete_id: UUID1,
        db: Connection,
    ) -> AthleteRead:
        return await super().get_object_by_id(
            tenant_id,
            athlete_id,
            db,
        )

    async def create_athlete(
        self,
        tenant_id: str,
        athlete: AthleteCreate,
        db: Connection,
    ) -> AthleteRead:
        return await super().create_object(
            tenant_id,
            athlete,
            db,
        )

    async def update_athlete(
        self,
        tenant_id: str,
        athlete: AthleteUpdate,
        db: Connection,
    ) -> AthleteRead:
        return await super().update_object(
            tenant_id,
            athlete,
            db,
        )

    async def delete_athlete(
        self,
        tenant_id: str,
        athlete_id: UUID1,
        db: Connection,
    ) -> None:
        return await super().delete_object(
            tenant_id,
            athlete_id,
            db,
        )

    async def get_all_athletes(
        self, tenant_id: str, db: Connection
    ) -> list[AthleteRead]:
        return await super().get_all_objects(tenant_id, db)

    async def get_all_athletes_updated_after(
        self,
        tenant_id: str,
        last_updated_at: datetime,
        db: Connection,
    ) -> list[AthleteRead]:
        return await super().get_all_objects_updated_after(
            tenant_id, last_updated_at, db
        )
