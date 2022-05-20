from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

# from models.admin import Admin
# from models.student import Student
from auth.models import User
from dashboard.models.dasboard import Dashboard
from dashboard.schemas.tags import Tag


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = None

    # JWT
    SECRET_KEY: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        orm_mode = True


# async def initiate_database():
#     try:
#         client = AsyncIOMotorClient(Settings().DATABASE_URL)
#         await init_beanie(
#             database=client.get_default_database(),
#             document_models=[User, Dashboard]
#         )
#         return client
#     except Exception as e:
#         print("Error connection to database: ", e)



class InitiateDatabase():
    def __int__(self):
        self.client: AsyncIOMotorClient | None = None

    async def get_db(self, db_name: str):
        try:
            db = self.client[db_name]
        except:
            db = None
        return db

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

initdb = InitiateDatabase()


# async def close_database(client):
#     client.close()
