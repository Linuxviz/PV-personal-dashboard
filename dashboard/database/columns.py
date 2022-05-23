import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from config.config import db as mongodb
from dashboard.models.dasboard import Dashboard
from dashboard.schemas.columns import Column, ColumnCreate
from dashboard.schemas.tags import Tag, TagUpdate


async def get_columns(dashboard_id: PydanticObjectId) -> List[Column]:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {
        'columns': 1, '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['columns']


async def try_to_create_column(dashboard_id: PydanticObjectId, column: ColumnCreate, collection):
    is_created: bool = False
    id = uuid.uuid4()
    new_column = Column(**column.dict(), id=id)
    find_query = {
        "_id": dashboard_id,
        "columns.id": {"$ne": id},
        "columns.name": {"$ne": column.name}
    }
    update_query = {
        '$push': {'columns': new_column.dict()}
    }
    result = await collection.update_one(find_query, update_query)
    if result.modified_count == 1:
        is_created = True
    return {'status': is_created, 'new_column': new_column}


async def create_column(dashboard_id: PydanticObjectId, column: ColumnCreate) -> Column:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    new_column = None
    for _ in range(3):
        result = await try_to_create_column(dashboard_id, column, collection)
        if result['status']:
            new_column = result['new_column']
            break
    if not new_column:
        raise HTTPException(status_code=400, detail='Can not create column with uniq name and id')
    return new_column


async def get_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID) -> Column:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
        "columns.id": column_id,
    }
    projection_query = {
        "columns.$": 1
    }
    result = await collection.find_one(find_query, projection_query)
    if result:
        return result['columns'][0]


async def update_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID, column: Column) -> Column:
    pass


async def delete_column(dashboard_id: PydanticObjectId, column_id: uuid.UUID) -> List[Column]:
    pass
