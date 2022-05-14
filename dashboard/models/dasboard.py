from types import NoneType
from typing import List

from beanie import Document

from dashboard.models.columns import Column
from dashboard.models.issues import Issue
from dashboard.models.tags import Tag


class Dashboard(Document):
    name: str
    background_url: str|NoneType = None
    tags: List[Tag]
    columns: List[Column]
    issues: List[Issue]

    class Config:
        schema_extra = {
            "example": {
                'name': 'dashboard_name',
                'background_url': '/test/uri',
                'tags': [Tag.Config.schema_extra, ],
                'columns': [Column.Config.schema_extra],
                'issues': [Issue.Config.schema_extra],
            }
        }
