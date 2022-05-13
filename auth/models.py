from typing import List

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr

from dashboard.models.dasboard import Dashboard


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    dashboards: List[Dashboard]

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Name Second_name",
                "email": "some@mail.dev",
                "password": "1"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
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
