from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from dashboard.models.dasboard import Dashboard
from dashboard.schemas.tags import Tag


async def get_tags(dashboard_id: PydanticObjectId) -> List[Tag]:
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find current dashboard")
    return dashboard.tags


async def create_tag(dashboard_id: PydanticObjectId, tag: Tag) -> Tag:
    dashboard = await Dashboard.get(dashboard_id)
    tags_names = {exist_tag.name for exist_tag in dashboard.tags}
    if tag.name in tags_names:
        raise HTTPException(status_code=400, detail="tag name must be uniq")
    update_query = {"$push": {
        'tags': tag
    }}
    if dashboard:
        await dashboard.update(update_query)
        return tag
