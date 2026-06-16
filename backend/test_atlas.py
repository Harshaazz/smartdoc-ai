from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

async def test():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))

    db = client[os.getenv("DATABASE_NAME")]

    result = await db.test.insert_one({
        "message": "Atlas connection works"
    })

    print("Inserted ID:", result.inserted_id)

asyncio.run(test())
print("URI loaded:", os.getenv("MONGO_URI"))