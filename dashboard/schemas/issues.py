import datetime
from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from dashboard.schemas.columns import Column

from dashboard.schemas.tags import Tag


class Issue(BaseModel):
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    creator: PydanticObjectId
    executor: PydanticObjectId
    tags: List[Tag] = []
    column: Column

    # meta_data: None = None  # Это поле в будущем будет ссылкой на другой документ в базе который будет аккамулировать данные для анализа
    # comments_list None = None # Это поле для списка комментариев под тикетом

    class Config:
        schema_extra = {
            "example": {
                'name': 'Issue',
                'description': 'Color',
                'tags': [Tag.Config.schema_extra],
                'column': [Column.Config.schema_extra],
            }
        }
