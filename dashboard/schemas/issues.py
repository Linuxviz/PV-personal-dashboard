import datetime
import uuid
from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from dashboard.schemas.columns import Column

from dashboard.schemas.tags import Tag


class Issue(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # creator: PydanticObjectId
    # executor: PydanticObjectId
    tags_ids: List[uuid.UUID] = []
    column_id: uuid.UUID

    # meta_data: None = None  # Это поле в будущем будет ссылкой на другой документ в базе который будет аккамулировать данные для анализа
    # comments_list None = None # Это поле для списка комментариев под тикетом

    class Config:
        schema_extra = {
            "example": {
                'name': 'Issue',
                'description': 'Color',
                'tags': [],
                'column': None,
            }
        }


class IssueCreate(BaseModel):
    name: str
    description: str | None = None
    # executor: PydanticObjectId | None = None в будущем
    tags_ids: List[uuid.UUID] = []
    column_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                'name': 'Issue',
                'description': 'Color',
                'tags_ids': [Tag.Config.schema_extra],
                'column_id': [Column.Config.schema_extra],
            }
        }


class IssueUpdate(BaseModel):
    # FIXME надо подумать о методах
    name: str
    description: str | None = None
    # executor: PydanticObjectId | None = None в будущем
    tags_ids: List[uuid.UUID] = None
    column_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                'name': 'Issue',
                'description': 'Color',
                'tags_ids': [],
            }
        }


class UpdateColumnInIssueData(BaseModel):
    column_id: uuid.UUID
    columns_ids: List[uuid.UUID]
