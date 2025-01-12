from asyncio import get_event_loop

from app.core.database import db, get_db


async def create_athlete_status(name: str):
    await db.connect()
    try:
        async with db.pool.acquire() as connection:
            db_ = connection
        await db_.execute(
            "INSERT INTO athlete_status (id, name) VALUES (5f0e92e2-d123-11ef-9cd2-0242ac120002, $1)",
            name,
        )
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(create_athlete_status("Active"))
    loop.close()
