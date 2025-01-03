from datetime import datetime

import orjson
from asyncpg import Connection, UniqueViolationError
from pydantic import UUID1

from app.core.base_schema import BaseSchema
from app.core.exceptions import (
    AlreadyExistsError,
    AlreadyUpdatedError,
    NotFoundError,
    UniqueViolationErrorHTTP,
)
from app.core.sse.broadcast import broadcast as global_broadcast
from app.core.sse.schemas import LocalActionEnum, SSEEvent
from app.core.utils.sql_utils import (
    convert_uuid_to_str,
    generate_sql_delete_with_returning,
    generate_sql_insert_with_returning,
    generate_sql_read,
    generate_sql_update_with_returning,
)


class DefaultService:
    def __init__(
        self,
        table_name: str,
        broadcast_endpoint: str,
        read_model: BaseSchema,
    ):
        self.broadcast = global_broadcast
        self.table = table_name
        self.broadcast_endpoint = broadcast_endpoint
        self.read_model = read_model

    async def notify_update(self, id: UUID1) -> None:
        event = SSEEvent(
            table_name=self.table,
            endpoint=self.broadcast_endpoint,
            id=id,
            local_action=LocalActionEnum.upsert,
        )
        await self.broadcast.publish(
            channel="update",
            message=orjson.dumps(event.model_dump()).decode("utf-8"),
        )

    async def notify_delete(self, id: UUID1) -> None:
        event = SSEEvent(
            table_name=self.table,
            endpoint=None,
            id=id,
            local_action=LocalActionEnum.delete,
        )
        await self.broadcast.publish(
            channel="update",
            message=orjson.dumps(event.model_dump()).decode("utf-8"),
        )

    async def get_object_by_id(
        self,
        tenant_id: str,
        id: UUID1,
        db: Connection,
    ) -> dict | None:
        query, values = generate_sql_read(
            tenant_id,
            self.table,
            self.read_model.model_fields.keys(),
            {"id": id},
        )
        result = await db.fetchrow(query, *values)
        if not result:
            return None
        return convert_uuid_to_str(dict(result))

    async def read_object_by_id(
        self,
        tenant_id: str,
        id: UUID1,
        db: Connection,
    ) -> dict:
        result = await self.get_object_by_id(tenant_id, id, db)
        if not result:
            raise NotFoundError(self.table, id)
        return result

    async def create_object(
        self,
        tenant_id: str,
        data: dict,
        db: Connection,
    ) -> dict:
        result = await self.get_object_by_id(tenant_id, data["id"], db)
        if result:
            raise AlreadyExistsError(self.table, data["id"])

        query, values = generate_sql_insert_with_returning(
            tenant_id,
            self.table,
            data,
            self.read_model.model_fields.keys(),
        )
        try:
            result = await db.fetchrow(query, *values)
            await self.notify_update(data["id"])
            return convert_uuid_to_str(dict(result))
        except UniqueViolationError:
            raise UniqueViolationErrorHTTP(self.table, data["id"])

    async def update_object(
        self,
        tenant_id: str,
        data: dict,
        db: Connection,
    ) -> dict:
        result = await self.get_object_by_id(tenant_id, data["id"], db)
        if not result:
            raise NotFoundError(self.table, data["id"])

        # TODO write util to convert the string to datetime
        if result["updated_at"] > data["updated_at"]:
            raise AlreadyUpdatedError(self.table, data["id"])
        result["updated_at"] = datetime.now()

        query, values = generate_sql_update_with_returning(
            tenant_id,
            self.table,
            data,
            {"id": data["id"]},
            self.read_model.model_fields.keys(),
        )
        try:
            result = await db.fetchrow(query, *values)
            await self.notify_update(data["id"])
            return convert_uuid_to_str(dict(result))
        except UniqueViolationError:
            raise UniqueViolationErrorHTTP(self.table, data["id"])

    async def delete_object(
        self,
        tenant_id: str,
        id: UUID1,
        db: Connection,
    ) -> None:
        result = await self.get_object_by_id(tenant_id, id, db)
        if not result:
            raise NotFoundError(self.table, id)

        query, values = generate_sql_delete_with_returning(
            tenant_id,
            self.table,
            {"id": id},
        )
        await db.execute(query, *values)
        await self.notify_delete(id)
        return None

    async def get_all_objects(self, tenant_id: str, db: Connection) -> list[dict]:
        query, values = generate_sql_read(
            tenant_id,
            self.table,
            self.read_model.model_fields.keys(),
        )
        results = await db.fetch(query, *values)
        return [convert_uuid_to_str(dict(result)) for result in results]