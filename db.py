from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection settings
MONGO_HOST = "mongodb+srv://silbereytan:Oodw8lpWfhcq4pf6@cluster0.bopuiwy.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "blog_db"

# Dependency to get the MongoDB database


async def get_database():
    client = AsyncIOMotorClient(MONGO_HOST)
    db = client[MONGO_DB]
    return db
