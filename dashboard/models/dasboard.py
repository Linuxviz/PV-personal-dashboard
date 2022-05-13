from typing import List

from beanie import Document

from dashboard.models.columns import Column
from dashboard.models.issues import Issue
from dashboard.models.tags import Tag


class Dashboard(Document):
    name: str
    background_url: str
    tags: List[Tag]
    columns: List[Column]
    issues: List[Issue]

    class Config:
        schema_extra = {
            "example": {
                'name': 'tag_name',
                'color': 'Color'
            }
        }
