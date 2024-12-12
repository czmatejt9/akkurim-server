from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI

from app.config import settings


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

    async def get_connection(self):
        async with self.pool.acquire() as connection:
            yield connection
            await connection.close()


db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
        app.state.db = db
        yield
    finally:
        await db.disconnect()


@asynccontextmanager
async def get_db():
    yield db.pool
