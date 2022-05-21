import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from config.config import db as mongodb
from dashboard.models.dasboard import Dashboard
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
    """name tag must be uniq, one of color or name must be"""
    print(tag.dict())
    #FIXME сделать более общий подход что бы словарь проматывался и подсатвлялся а если есть имя то
    #нужно добавлять условие по имени
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "tags.id": tag_id
    }
    update_query = {'$set': None}
    print("______________", dir(tag))
    if tag.name is not None:
        find_query['tags.name'] = {"$ne": f'{tag.name}'}
        if tag.name is not None:
            update_query = {
                '$set': {
                    'tags.$.color': f'{tag.color}',
                    'tags.$.name': f'{tag.name}'
                }
            }
    else:
        update_query = {
            '$set': {
                'tags.$.color': f'{tag.color}',
            }
        }

    result = await collection.update_one(
        find_query,
        update_query
    )
    print("***********", result.acknowledged, result.matched_count, result.modified_count, "********")
