import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends

from auth.business.jwt_bearer import JWTBearer
from dashboard.database.issues import get_issue, get_issues, create_issue, delete_issue
from dashboard.schemas.issues import Issue, IssueCreate

# tags_metadata = [
#     {"name": "Get Methods", "description": "One other way around"},
#     {"name": "Post Methods", "description": "Keep doing this"},
#     {"name": "Delete Methods", "description": "KILL 'EM ALL"},
#     {"name": "Put Methods", "description": "Boring"},
# ]
#
# app = FastAPI(openapi_tags=tags_metadata)

from dashboard.views.issues.issues_columns import issues_columns_router
from dashboard.views.issues.issues_tags import issues_tags_router
from dashboard.views.issues.issues_text_fields import issues_text_fields_router

issues_router = APIRouter(prefix="/dashboard")
issues_router.include_router(issues_tags_router)
issues_router.include_router(issues_columns_router)
issues_router.include_router(issues_text_fields_router)


@issues_router.get('/{dashboard_id}/issue/{issues_id}', tags=['Issues', ], response_model=Issue)
async def get_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, credentials=Depends(JWTBearer())):
    """
    EN: Return issue data

    RU: Возвращает данные задачи
    """
    issue = await get_issue(dashboard_id, issue_id)
    if issue:
        return issue
    raise HTTPException(status_code=400, detail="Can not find the issue")


@issues_router.get(
    "/{dashboard_id}/issues",
    tags=['Issues', ],
    response_model=List[Issue])
async def get_issues_view(dashboard_id: PydanticObjectId, credentials=Depends(JWTBearer())):
    """
    EN: Return list of all created issues in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    issues = await get_issues(dashboard_id)
    return issues


@issues_router.post("/{dashboard_id}/issues", tags=['Issues', ], response_model=Issue)
async def set_issue_view(dashboard_id: PydanticObjectId, issue: IssueCreate, credentials=Depends(JWTBearer())):
    """
    EN: name must be uniq

    RU:
    """
    # TODO сделать проверку на права операции
    created_issue = await create_issue(dashboard_id, issue)
    if created_issue:
        return created_issue
    raise HTTPException(status_code=400, detail="Can not create issue")


@issues_router.delete(
    '/{dashboard_id}/issue/{issue_id}',
    tags=['Issues', ],
    response_model=List[Issue]
)  #
async def delete_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, credentials=Depends(JWTBearer())):
    """
    EN:

    RU:
    """
    issues = await delete_issue(dashboard_id, issue_id)
    return issues
