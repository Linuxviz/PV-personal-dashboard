from typing import List, Optional

from beanie import Document
from pydantic import BaseModel

from dashboard.models.columns import Column
from dashboard.models.issues import Issue
from dashboard.models.tags import Tag
from dashboard.schemas.responses import Response


class Dashboard(Document):
    name: str
    background_url: Optional[str] = None
    tags: List[Tag] = []
    columns: List[Column] = []
    issues: List[Issue] = []

    class Collection:
        name = "dashboard"

    class Config:
        schema_extra = {
            "example": {
                'name': 'dashboard_name',
                'background_url': '/test/uri',
                'tags': [Tag.Config.schema_extra, ],
                'columns': [Column.Config.schema_extra, ],
                'issues': [Issue.Config.schema_extra, ],
            }
        }


class DashboardCreate(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'dashboard_name',
                'background_url': '/test/uri',
            }
        }


class DashboardCreateResponse(Response):
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
