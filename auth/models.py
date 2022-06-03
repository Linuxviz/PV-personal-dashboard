from beanie import Document
from pydantic import BaseModel, EmailStr

from auth.schemas import DashboardsIds


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    dashboards: DashboardsIds = DashboardsIds(
        owner_dashboards_ids=[],
        member_dashboards_ids=[],
        observer_dashboards_ids=[]
    )

    class Collection:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Name Second_name",
                "email": "some@mail.dev",
                "password": "1"
            }
        }


class AdminSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "some@mail.dev",
                "password": "1"
            }
        }


class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Name Second_name",
                "email": "some@mail.dev",
            }
        }
