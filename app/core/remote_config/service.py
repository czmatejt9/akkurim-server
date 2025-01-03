from asyncpg import Connection

from app.core.remote_config.exceptions import RemoteConfigNotFoundError
from app.core.utils import convert_uuid_to_str, generate_sql_read


class RemoteConfigService:
    def __init__(self) -> None:
        self.table = "remote_config"

    async def get_remote_config(self, tenant_id: str, db: Connection) -> dict:
        query, values = generate_sql_read(
            tenant_id,
            self.table,
            ["welcome_message", "minimum_app_version"],
        )
        remote_config = await db.fetchrow(query, *values)
        if not remote_config:
            raise RemoteConfigNotFoundError(tenant_id)

        return convert_uuid_to_str(dict(remote_config))
