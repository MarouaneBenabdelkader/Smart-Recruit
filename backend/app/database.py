from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from config import settings

client: AsyncIOMotorClient = None


def get_database():
    return client[settings.database_name]


async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(
        settings.mongodb_url,
        maxPoolSize=settings.max_connection_pool_size,
        minPoolSize=settings.min_connection_pool_size,
    )
    print("Connected to MongoDB")


async def close_mongo_connection():
    client.close()
    print("Closed connection with MongoDB")


def create_start_app_handler(app: FastAPI) -> callable:
    async def start_app() -> None:
        await connect_to_mongo()
        app.state.client = client  # Storing client in app state for global access

    return start_app


def create_stop_app_handler(app: FastAPI) -> callable:
    async def stop_app() -> None:
        await close_mongo_connection()

    return stop_app
