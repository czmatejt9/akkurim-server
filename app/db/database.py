import asyncpg
from fastapi import FastAPI

from app.config import settings


async def init_db(app: FastAPI):
    app.state.db = await asyncpg.create_pool(dsn=settings.DATABASE_URL)

    yield
    await app.state.db.close()
