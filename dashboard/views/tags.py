import uuid

from beanie import PydanticObjectId
from fastapi import APIRouter
from dashboard.database.tags import get_tags, create_tag, update_tag
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


@tags_router.patch("dashboard/{dashboard_id}/tag/{tag_name}", tags=['tags', ] )#,response_model=TagChangeResponse
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

# TODO need delete tag, bun before need delete tag from issues.
