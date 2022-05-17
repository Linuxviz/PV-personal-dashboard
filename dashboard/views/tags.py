from beanie import PydanticObjectId
from fastapi import APIRouter
from dashboard.database.database import add_tag
from dashboard.models.tags import Tag

tags_router = APIRouter()


@tags_router.get("{dashboard_id}/tag/{tag_id}", tags=['tags', ])
async def tag(dashboard_id: PydanticObjectId, tag_id: PydanticObjectId):
    """
    EN:
    RU: Ищет выбранный тэг в конкретной доске
    """
    # new_student = await collection_lo["students"].insert_one({'boba':tag_id})
    # created_student = await collection_lo["students"].find_one({"_id": new_student.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

    return {"message": f"Данные о тэге "}  # created_student


@tags_router.post("{dashboard_id}/tag", tags=['tags', ])
async def tag(dashboard_id: PydanticObjectId, tag: Tag):
    """
    EN:
    RU: Создает тэг в выбранном дашборде
    """
    tag = await add_tag(dashboard_id, tag)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Tag created successfully",
        "tag": tag
    }


@tags_router.get("/tags", tags=['tags', ])
async def tags():
    """
    EN:
    RU:
    """
    return {"message": "Список тэгов"}
