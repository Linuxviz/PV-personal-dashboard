import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from dashboard.database.columns import create_column, update_column, delete_column, get_columns, get_column
from dashboard.schemas.columns import Column

columns_router = APIRouter()


@columns_router.get('/dashboard/{dashboard_id}/column/{column_id}', tags=['columns', ], response_model=Column)
async def get_tag_view(dashboard_id: PydanticObjectId, column_id: uuid.UUID):
    """
    EN:

    RU:
    """
    column = await get_column(dashboard_id, column_id)
    if column:
        return column
    raise HTTPException(status_code=400, detail="Can not find the tag")


@columns_router.get(
    "/dashboard/{dashboard_id}/columns",
    tags=['columns', ],
    response_model=List[Column])
async def get_columns_view(dashboard_id: PydanticObjectId):
    """
    EN: Return list of all created tags in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    columns = await get_columns(dashboard_id)
    return columns


@columns_router.post("/dashboard/{dashboard_id}/column", tags=['columns', ], response_model=Column)
async def set_column_view(dashboard_id: PydanticObjectId, column: Column):
    """
    EN:

    RU:
    """
    # TODO сделать проверку на права операции
    created_column = await create_column(dashboard_id, column)
    if created_column:
        return created_column
    raise HTTPException(status_code=400, detail="Can not create column")


@columns_router.patch("/dashboard/{dashboard_id}/column/{column_id}", tags=['columns'], response_model=Column)
async def update_column_view(dashboard_id: PydanticObjectId, column_id: uuid.UUID, column: Column):
    """
    EN:

    RU:
    """
    updated_column = await update_column(dashboard_id, column_id, column)
    if updated_column:
        return updated_column
    raise HTTPException(status_code=400, detail="Can not update column")


@columns_router.delete(
    '/dashboard/{dashboard_id}/column/{column_id}',
    tags=['columns', ],
    response_model=List[Column]
)  #
async def delete_column_view(dashboard_id: PydanticObjectId, column_id: uuid.UUID):
    """
    EN: Delete tag in dashboard, and return list of tags. If all tags id deletes will return empty list "[]"

    RU:
    # TODO need delete tag, bun before need delete tag from issues.
    """
    columns = await delete_column(dashboard_id, column_id)
    return columns
