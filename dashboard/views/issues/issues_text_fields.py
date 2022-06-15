import uuid

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, APIRouter

from auth.business.jwt_bearer import JWTBearer
from dashboard.database.issues import update_issue_name, update_issue_description
from dashboard.schemas.issues import Issue

issues_text_fields_router = APIRouter()


@issues_text_fields_router.put(
    '/{dashboard_id}/issue/{issue_id}/name',
    tags=['issues-text-fields', ],
    response_model=Issue
)
async def update_name_view(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        name: str,
        credentials=Depends(JWTBearer())
) -> Issue:
    updated_issue = await update_issue_name(dashboard_id, issue_id, name)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Cant update issue name")


@issues_text_fields_router.put(
    '/{dashboard_id}/issue/{issue_id}/description',
    tags=['issues-text-fields', ],
    response_model=Issue
)
async def update_description_view(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        description: str,
        credentials=Depends(JWTBearer())
) -> Issue:
    updated_issue = await update_issue_description(dashboard_id, issue_id, description)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Can't update issue description")
