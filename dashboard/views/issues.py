import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends

from auth.business.jwt_bearer import JWTBearer
from dashboard.database.issues import get_issue, get_issues, create_issue, update_issue, delete_issue, \
    change_column_for_issue, get_data_for_update_column_in_issue
from dashboard.schemas.issues import Issue, IssueCreate, IssueUpdate
from dashboard.business.issues_columns import check_update_columns_conditions

# tags_metadata = [
#     {"name": "Get Methods", "description": "One other way around"},
#     {"name": "Post Methods", "description": "Keep doing this"},
#     {"name": "Delete Methods", "description": "KILL 'EM ALL"},
#     {"name": "Put Methods", "description": "Boring"},
# ]
#
# app = FastAPI(openapi_tags=tags_metadata)
#
#
# @app.delete("/items", tags=["Delete Methods"])
# @app.put("/items", tags=["Put Methods"])
# @app.post("/items", tags=["Post Methods"])
# @app.get("/items", tags=["Get Methods"])


issues_router = APIRouter(prefix="/dashboard")


@issues_router.get('/{dashboard_id}/issue/{issues_id}', tags=['issues', ], response_model=Issue)
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
    tags=['issues', ],
    response_model=List[Issue])
async def get_issues_view(dashboard_id: PydanticObjectId, credentials=Depends(JWTBearer())):
    """
    EN: Return list of all created issues in current dashboard

    RU:
    """
    # TODO сделать проверку на права операции
    issues = await get_issues(dashboard_id)
    return issues


@issues_router.post("/{dashboard_id}/issues", tags=['issues', ], response_model=Issue)
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
    tags=['issues', ],
    response_model=List[Issue]
)  #
async def delete_issue_view(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, credentials=Depends(JWTBearer())):
    """
    EN:

    RU:
    """
    issues = await delete_issue(dashboard_id, issue_id)
    return issues


@issues_router.patch('/{dashboard_id}/issue/{issue_id}/', tags=['issues', ], )
async def update_issue():
    """You can patch only non choices values"""
    pass


@issues_router.put('/{dashboard_id}/issue/{issue_id}/', tags=['issues', ], )
async def replace_issue():
    """Update, full replace issue"""
    pass


### TAGS ###
# TODO replace in new document and maybe in new router


@issues_router.get('/{dashboard_id}/issue/{issue_id}/tags', tags=['issues-tags', ], )
async def get_issue_tags():
    """Return tags for current issue"""
    pass


@issues_router.post('/{dashboard_id}/issue/{issue_id}/tags', tags=['issues-tags', ], )
async def add_issue_tags():
    """Add tags for issue"""
    pass


@issues_router.delete('/{dashboard_id}/issue/{issue_id}/tags', tags=['issues-tags', ], )
async def pop_issue_tags():
    """Pull tags for issue"""
    pass


@issues_router.put('/{dashboard_id}/issue/{issue_id}/tags', tags=['issues-tags', ], )
async def set_issue_tags():
    """Set tags for issue(replace)"""
    pass


### COLUMNS ###
# TODO replace in new document and maybe in new router

@issues_router.patch(
    '/{dashboard_id}/issue/{issue_id}/column/{column_id}',
    tags=['issues-columns', ],
    response_model=Issue
)
async def update_issue_column(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, column_id: uuid.UUID):
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
