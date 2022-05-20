import pprint
import uuid
from typing import List

from beanie import PydanticObjectId
from beanie.odm.operators.find.comparison import In
from fastapi import HTTPException

from config.config import InitiateDatabase, initdb
from dashboard.models.dasboard import Dashboard
from dashboard.schemas.tags import Tag, TagUpdate

x = initdb

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
    db = await x.get_db('mongodb')
    collection = db['dashboard']
    result = await collection.update_one(
        {
            "_id": dashboard_id,
            "tags.id": tag_id
        },
        {
            '$set': {'tags.$.color': 'orange'}
        }
    )
