import asyncpg
from asyncpg import Connection

from app.core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=settings.MIN_CONNECTIONS,
            max_size=settings.MAX_CONNECTIONS,
        )

    async def disconnect(self):
        await self.pool.close()


db = Database()


async def get_db():
    async with db.pool.acquire() as connection:
        try:
            yield connection
        finally:
            connection: Connection
            await connection.close()
