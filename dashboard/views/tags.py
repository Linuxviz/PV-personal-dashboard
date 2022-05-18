from beanie import PydanticObjectId
from fastapi import APIRouter
from dashboard.database.tags import get_tags, create_tag
from dashboard.schemas.tags import Tag, TagListResponse, TagCreateResponse

tags_router = APIRouter()


@tags_router.get(
    "/{dashboard_id}/tags",
    tags=['tags', ],
    response_model=TagListResponse)
async def tags(dashboard_id: PydanticObjectId):
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


@tags_router.post("/{dashboard_id}/tag", tags=['tags', ], response_model=TagCreateResponse)
async def tags(dashboard_id: PydanticObjectId, tag: Tag):
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

# @tags_router.get("/{dashboard_id}/tag/{tag_id}", tags=['tags', ])
# async def tag(dashboard_id: PydanticObjectId, tag_id: PydanticObjectId):
#     """
#     EN:
#     RU: Ищет выбранный тэг в конкретной доске
#     """
#     # new_student = await collection_lo["students"].insert_one({'boba':tag_id})
#     # created_student = await collection_lo["students"].find_one({"_id": new_student.inserted_id})
#     # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
#
#     return {"message": f"Данные о тэге "}  # created_student


# @tags_router.post("{dashboard_id}/tag", tags=['tags', ])
# async def tag(dashboard_id: PydanticObjectId, tag: Tag):
#     """
#     EN:
#     RU: Создает тэг в выбранном дашборде
#     """
#     tag = await add_tag(dashboard_id, tag)
#     return {
#         "status_code": 200,
#         "response_type": "success",
#         "description": "Tag created successfully",
#         "tag": tag
#     }
