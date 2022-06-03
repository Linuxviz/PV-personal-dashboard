from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel


class DashboardsIds(BaseModel):
    owner_dashboards_ids: List[PydanticObjectId] = []
    member_dashboards_ids: List[PydanticObjectId] = []
    observer_dashboards_ids: List[PydanticObjectId] = []
