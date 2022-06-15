import uuid

from beanie import PydanticObjectId
from fastapi import HTTPException, APIRouter

from dashboard.business.issues_columns import check_update_columns_conditions
from dashboard.database.issues import get_data_for_update_column_in_issue, change_column_for_issue
from dashboard.schemas.issues import Issue

issues_columns_router = APIRouter()


@issues_columns_router.patch(
    '/{dashboard_id}/issue/{issue_id}/column/{column_id}',
    tags=['issues-columns', ],
    response_model=Issue
)
async def update_issue_column_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, column_id: uuid.UUID):
    """
    EN: Change column for issue

    RU:
    """
    data = await get_data_for_update_column_in_issue(dashboard_id, issue_id)
    await check_update_columns_conditions(
        new_column_id=column_id,
        columns_ids=data.columns_ids,
        old_column_id=data.column_id,
    )
    updated_issue = await change_column_for_issue(dashboard_id, issue_id, column_id)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Can not create change issue id")
