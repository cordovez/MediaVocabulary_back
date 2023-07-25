from db.db import init_db

async def connect():
    await init_db()

if __name__ == "__run-spider__":
    connect()