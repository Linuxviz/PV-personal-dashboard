import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from dashboard.database.tags import get_tags, create_tag, update_tag, delete_tag, get_tag
from dashboard.schemas.tags import Tag, TagListResponse, TagChangeResponse, TagUpdate

tags_router = APIRouter()


@tags_router.get(
    "/dashboard/{dashboard_id}/tags",
    tags=['tags', ],
    response_model=TagListResponse)
async def get_tags_view(dashboard_id: PydanticObjectId):
    """
    EN: Return list of all created tags in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    tags = await get_tags(dashboard_id)
    return {
        "tags": tags,
        "status_code": 200,
        "response_type": "success",
        "description": "The list of tags data",
    }


@tags_router.post("/dashboard/{dashboard_id}/tag", tags=['tags', ], response_model=TagChangeResponse)
async def set_tag_view(dashboard_id: PydanticObjectId, tag: Tag):
    """
    EN: Return list of all created tags in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    tag = await create_tag(dashboard_id, tag)
    if tag:
        return {
            "tag": tag,
            "status_code": 200,
            "response_type": "success",
            "description": "The list of tags data",
        }
    return {
        "tag": tag,
        "status_code": 400,
        "response_type": "error",
        "description": "Can not crate tag",
    }


@tags_router.patch("dashboard/{dashboard_id}/tag/{tag_id}", tags=['tags'], response_model=TagChangeResponse)
async def update_tag_view(dashboard_id: PydanticObjectId, tag_id: uuid.UUID, tag: TagUpdate):
    """
    EN:

    RU:

    :param dashboard_id:
    :param tag_id:
    :param tag:
    :return:
    """
    updated_tag = await update_tag(dashboard_id, tag_id, tag)
    if updated_tag:
        return {
            "tag": updated_tag,
            "status_code": 200,
            "response_type": "success",
            "description": "Tag update successfully",
        }
    return {
        "tag": tag,
        "status_code": 400,
        "response_type": "error",
        "description": "Can not update tag",
    }


@tags_router.delete('/dashboard/{dashboard_id}/tag/{tag_id}', tags=['tags', ], response_model=List[Tag])  #
async def delete_tag_view(dashboard_id: PydanticObjectId, tag_id: uuid.UUID):
    """
    EN: Delete tag in dashboard, and return list of tags. If all tags id deletes will return empty list "[]"

    RU:
    # TODO need delete tag, bun before need delete tag from issues.
    """
    deleted_tag = await delete_tag(dashboard_id, tag_id)
    if deleted_tag or len(deleted_tag) == 0:
        return deleted_tag
    raise HTTPException(status_code=400, detail="Can not find tag for deleting")


@tags_router.get('/dashboard/{dashboard_id}/tag/{tag_id}', tags=['tags', ], response_model=Tag)
async def get_tag_view(dashboard_id: PydanticObjectId, tag_id: uuid.UUID):
    """
    EN:

    RU:
    """
    tag = await get_tag(dashboard_id, tag_id)
    if tag:
        return tag
    raise HTTPException(status_code=400, detail="Can not find the tag")

