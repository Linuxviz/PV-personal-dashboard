from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from dashboard.models.dasboard import Dashboard
from dashboard.schemas.responses import Response


class DashboardCreate(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'dashboard_name',
            }
        }


class DashboardCreateResponse(Response):
    """
    EN: For creating dashboard we need name.

    RU:
    """
    dashboard: Dashboard

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "dashboard": Dashboard.Config.schema_extra
            }
        }


class DashboardListResponse(Response):
    dashboards_ids: List[PydanticObjectId]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "dashboards": []
            }
        }