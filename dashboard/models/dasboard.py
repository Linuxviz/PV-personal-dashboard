from typing import List, Optional

from beanie import Document

from dashboard.schemas.columns import Column
from dashboard.schemas.issues import Issue
from dashboard.schemas.tags import Tag


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
