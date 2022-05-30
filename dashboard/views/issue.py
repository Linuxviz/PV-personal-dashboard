import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from dashboard.database.issues import get_issue, get_issues, create_issue, update_issue, delete_issue
from dashboard.schemas.issues import Issue, IssueCreate, IssueUpdate

issues_router = APIRouter()


@issues_router.get('/dashboard/{dashboard_id}/issue/{issues_id}', tags=['issues', ], response_model=Issue)
async def get_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID):
    """
    EN: Return issue data

    RU: Возвращает данные задачи
    """
    issue = await get_issue(dashboard_id, issue_id)
    if issue:
        return issue
    raise HTTPException(status_code=400, detail="Can not find the issue")


@issues_router.get(
    "/dashboard/{dashboard_id}/issues",
    tags=['issues', ],
    response_model=List[Issue])
async def get_issues_view(dashboard_id: PydanticObjectId):
    """
    EN: Return list of all created issues in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    issues = await get_issues(dashboard_id)
    return issues


@issues_router.post("/dashboard/{dashboard_id}/issues", tags=['issues', ], response_model=Issue)
async def set_issue_view(dashboard_id: PydanticObjectId, issue: IssueCreate):
    """
    EN: name must be uniq

    RU:
    """
    # TODO сделать проверку на права операции
    created_issue = await create_issue(dashboard_id, issue)
    if created_issue:
        return created_issue
    raise HTTPException(status_code=400, detail="Can not create issue")


@issues_router.patch("/dashboard/{dashboard_id}/issue/{issue_id}", tags=['issues'], response_model=Issue)
async def update_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, issue: IssueUpdate):
    """
    EN:

    RU:
    """
    updated_issue = await update_issue(dashboard_id, issue_id, issue)
    if updated_issue:
        return updated_issue
    raise HTTPException(status_code=400, detail="Can not update issue")


@issues_router.delete(
    '/dashboard/{dashboard_id}/issue/{issue_id}',
    tags=['issues', ],
    response_model=List[Issue]
)  #
async def delete_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID):
    """
    EN:

    RU:
    """
    issues = await delete_issue(dashboard_id, issue_id)
    return issues
