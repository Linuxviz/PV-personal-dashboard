from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel


class UsersIds(BaseModel):
    owner_id: PydanticObjectId
    member_ids: List[PydanticObjectId] = []
    observer_ids: List[PydanticObjectId] = []


class DashboardCreate(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'dashboard_name',
            }
        }
