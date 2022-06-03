from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from auth.models import User
from dashboard.models.dashboard import Dashboard


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    SECRET_KEY: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        orm_mode = True


class DataBase:
    def __int__(self):
        self.client: AsyncIOMotorClient | None = None

    async def get_db(self, db_name: str) -> AsyncIOMotorClient | None:
        try:
            current_db = self.client[db_name]
        except:
            current_db = None
        return current_db

    async def get_collection(self, db_name: str, collection_name: str):
        try:
            current_db = self.client[db_name]
            collection = current_db[collection_name]
            return collection
        except Exception as e:
            print("Error getting db collection: ", e)

    async def initiate_database(self):
        try:
            self.client = AsyncIOMotorClient(Settings().DATABASE_URL)
            await init_beanie(
                database=self.client.get_default_database(),
                document_models=[User, Dashboard]
            )
            return self.client
        except Exception as e:
            print("Error connection to database: ", e)


db = DataBase()

# async def close_database(client):
#     client.close()
