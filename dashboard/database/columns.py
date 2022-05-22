import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from config.config import db as mongodb
from dashboard.models.dasboard import Dashboard
from dashboard.schemas.columns import Column
from dashboard.schemas.tags import Tag, TagUpdate


async def get_columns(dashboard_id: PydanticObjectId) -> List[Column]:
    pass


async def create_column(dashboard_id: PydanticObjectId, column: Tag) -> Column:
    pass


async def update_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID, column: Column) -> Column:
    pass


async def delete_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID) -> List[Column]:
    pass


async def get_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID) -> Column:
    pass
