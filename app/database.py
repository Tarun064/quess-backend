from motor.motor_asyncio import AsyncIOMotorClient
import logging
from .config import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None
db = None

async def connect_db():
    global client, db
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000  # 5 seconds timeout
        )
        db = client[settings.DATABASE_NAME]
        
        # Ping the database to verify connection
        await client.admin.command('ping')
        print(f"Successfully connected to MongoDB at {settings.MONGODB_URI}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        # We don't raise here to allow the app to start, but database operations will fail
        # Alternatively, we could raise if the DB is critical
        # raise e

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_db():
    return db
