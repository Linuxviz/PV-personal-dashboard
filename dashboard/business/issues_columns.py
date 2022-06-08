import uuid
from typing import List

from fastapi import HTTPException


async def check_update_columns_conditions(
        new_column_id: uuid.UUID,
        columns_ids: List[uuid.UUID],
        old_column_id: uuid.UUID
) -> None:
    """
    columns_ids: list of id available in dashboard
    """
    if new_column_id not in columns_ids:
        raise HTTPException(
            detail="Column id do not in columns list in dashboard,"
                   " please check all available columns and try to use that ids.",
            status_code=400
        )
    if new_column_id == old_column_id:
        raise HTTPException(
            detail="You try to change column on itself",
            status_code=400
        )
