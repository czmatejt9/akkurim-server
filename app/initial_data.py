from app.core.database import get_db


async def create_athlete_status(name: str):
    db = await get_db()
    try:
        db.execute("INSERT INTO athlete_status (id, name) VALUES (1, $1)", name)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    create_athlete_status("Active")
