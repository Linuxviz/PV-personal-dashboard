import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException
from pymongo import UpdateOne

from config.config import db as mongodb
from dashboard.models.dashboard import Dashboard
from dashboard.schemas.tags import Tag, TagUpdate


async def get_tags(dashboard_id: PydanticObjectId) -> List[Tag]:
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find current dashboard")
    return dashboard.tags


async def create_tag(dashboard_id: PydanticObjectId, tag: Tag) -> Tag:
    dashboard = await Dashboard.get(dashboard_id)
    tags_id = {exist_tag.id for exist_tag in dashboard.tags}
    for _ in range(100):
        if tag.id in tags_id:
            tag.id = uuid.uuid4()
    if tag.id in tags_id:
        raise HTTPException(status_code=400, detail="Can not create uuid for tag")
    tags_names = {exist_tag.name for exist_tag in dashboard.tags}
    if tag.name in tags_names:
        raise HTTPException(status_code=400, detail="tag name must be uniq")
    update_query = {"$push": {
        'tags': tag
    }}
    if dashboard:
        await dashboard.update(update_query)
        return tag


async def update_tag(dashboard_id: PydanticObjectId, tag_id: uuid.UUID, tag: TagUpdate) -> Tag:
    """ name tag must be uniq, one of color or name must be """
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "tags.id": tag_id
    }
    update_query = {}
    fields = tag.dict()
    for field in fields:
        if fields[field] is not None:
            update_query[f'tags.$.{field}'] = f'{fields[field]}'
            if field == 'name':
                find_query[f'tags.{field}'] = {"$ne": f'{fields[field]}'}
    result = await collection.update_one(
        find_query,
        {'$set': update_query}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    result = await collection.find_one({"_id": dashboard_id}, {'_id': 0, 'tags': {'$elemMatch': {'id': tag_id}}})
    return Tag(**result['tags'][0])


async def delete_tag(dashboard_id: PydanticObjectId, tag_id: uuid.UUID) -> List[Tag]:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query_tags_list = {
        "_id": dashboard_id,
        "tags.id": tag_id
    }
    update_query_tags_list = {
        '$pull': {
            'tags': {'id': tag_id}
        }
    }
    find_query_tags_in_issue = {
        "_id": dashboard_id,
        "issues.tags_ids": tag_id,
    }
    update_query_tags_in_issue = {
        '$pull': {
            'issues.$.tags_ids': tag_id
        }
    }
    result = await collection.bulk_write([
        UpdateOne(find_query_tags_list, update_query_tags_list),
        UpdateOne(find_query_tags_in_issue, update_query_tags_in_issue),
    ])
    # TODO fix check of updating
    # if result.modified_count != 1:
    #     raise HTTPException(status_code=400, detail="something wrong")
    result = await collection.find_one({"_id": dashboard_id}, {'tags': 1, '_id': 0})
    return result['tags']


async def get_tag(dashboard_id: PydanticObjectId, tag_id: uuid.UUID):
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "tags.id": tag_id
    }
    projection_query = {"tags.$": 1}
    result = await collection.find_one(find_query, projection_query)
    return result['tags'][0]
