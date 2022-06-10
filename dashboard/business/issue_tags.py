import uuid
from typing import List

from fastapi import HTTPException

from dashboard.schemas.issues import AddTagInIssueData


async def check_add_tag_conditions(
        data: AddTagInIssueData,
        new_tag_id: uuid.UUID,
) -> None:
    """
    columns_ids: list of id available in dashboard
    """
    if new_tag_id not in data.tags_ids_in_dashboard:
        raise HTTPException(
            detail="Tag id do not in tags list in dashboard,"
                   " please check all available tags and try to use that ids.",
            status_code=400
        )
    if new_tag_id in data.tags_ids_in_issue:
        raise HTTPException(
            detail="You try to add tag already in issue.",
            status_code=400
        )


async def check_pop_tag_conditions(
        tags_ids_in_issue: List[uuid.uuid4],
        new_tag_id: uuid.UUID,
) -> None:
    """
    columns_ids: list of id available in dashboard
    """
    if new_tag_id not in tags_ids_in_issue:
        raise HTTPException(
            detail="Tag id do not in tags list in issue,"
                   " maybe tag already delete from issue?",
            status_code=400
        )
