from beanie import Document
from pydantic.color import Color


class Issue(Document):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'Issue',
                'color': 'Color'
            }
        }
