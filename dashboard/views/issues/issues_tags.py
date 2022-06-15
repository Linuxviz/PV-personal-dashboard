import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, APIRouter

from auth.business.jwt_bearer import JWTBearer
from dashboard.business.issue_tags import check_add_tag_conditions, check_pop_tag_conditions
from dashboard.database.issues import get_issue_tags, get_data_for_add_tag_in_issue, add_tag_for_issue, \
    get_data_for_pop_tag_from_issue, pop_tag_from_issue
from dashboard.schemas.issues import Issue

issues_tags_router = APIRouter()


@issues_tags_router.get(
    '/{dashboard_id}/issue/{issue_id}/tags',
    tags=['issues-tags', ],
    response_model=List[uuid.UUID]
)
async def get_issue_tags_view(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        credentials=Depends(JWTBearer())
):
    tags = await get_issue_tags_view(dashboard_id, issue_id)
    if tags:
        return tags
    raise HTTPException(status_code=400, detail="Can't find tags or issue")


@issues_tags_router.post(
    '/{dashboard_id}/issue/{issue_id}/tag/{tag_id}',
    tags=['issues-tags', ],
    response_model=Issue)
async def add_issue_tags(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        tag_id: uuid.UUID,
        credentials=Depends(JWTBearer())
):
    data = await get_data_for_add_tag_in_issue(dashboard_id, issue_id)
    await check_add_tag_conditions(data, tag_id)
    updated_issue = await add_tag_for_issue(dashboard_id, issue_id, tag_id)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Can't add tag to issue")


@issues_tags_router.delete(
    '/{dashboard_id}/issue/{issue_id}/tag/{tag_id}',
    tags=['issues-tags', ],
    response_model=Issue
)
async def pop_issue_tags(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        tag_id: uuid.UUID,
        credentials=Depends(JWTBearer())
) -> Issue:
    """Pull tags for issue"""
    data = await get_data_for_pop_tag_from_issue(dashboard_id, issue_id)
    await check_pop_tag_conditions(tags_ids_in_issue=data, new_tag_id=tag_id)
    updated_issue = await pop_tag_from_issue(dashboard_id, issue_id, tag_id)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Can't delete tag from issue")
