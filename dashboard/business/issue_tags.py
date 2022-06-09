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
            detail="Tag id do not in columns list in dashboard,"
                   " please check all available columns and try to use that ids.",
            status_code=400
        )
    if new_tag_id in data.tags_ids_in_issue:
        raise HTTPException(
            detail="You try to add tag already in issue.",
            status_code=400
        )
