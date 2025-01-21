from asyncpg import Connection
from pydantic import UUID1

from app.core.shared.schemas import SchoolYearCreate, SchoolYearRead
from app.core.utils.default_service import DefaultService
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_insert_with_returning,
    generate_sql_read,
    generate_sql_read_with_join_table,
)


class SchoolYearService(DefaultService):
    def __init__(self):
        super().__init__(
            "school_year",
            "/school_year/{id}",
            SchoolYearRead,
        )

    async def get_school_year_by_id(
        self,
        tenant_id: str,
        school_year_id: UUID1,
        db: Connection,
    ) -> SchoolYearRead:
        return await super().get_object_by_id(
            tenant_id,
            school_year_id,
            db,
        )

    async def create_school_year(
        self,
        tenant_id: str,
        school_year: SchoolYearCreate,
        db: Connection,
    ) -> SchoolYearRead:
        return await super().create_object(
            tenant_id,
            school_year,
            db,
        )

    async def get_all_school_years(
        self,
        tenant_id: str,
        db: Connection,
    ) -> list[SchoolYearRead]:
        return await super().get_all_objects(
            tenant_id,
            db,
        )
