from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from auth.models import User
from dashboard.models.dasboard import Dashboard
from dashboard.schemas.dashboards import DashboardCreate


async def get_dashboard(dashboard_id: PydanticObjectId) -> Dashboard:
    """
    EN: Return Dashboard

    RU:
    """
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find dashboard")
    return dashboard


async def get_dashboards(user_id: PydanticObjectId) -> List[PydanticObjectId]:
    """
    EN: Return list of ids dashboards current user

    RU:
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Can not find user"
        )
    return user.dashboards


async def create_dashboard(
        dashboard_data: DashboardCreate,
        user_id: PydanticObjectId
) -> Dashboard:
    """
    EN: When we create dashboard we should add dashboard to user model

    RU:
    """
    dashboard = Dashboard(**dashboard_data.dict())
    created_dashboard = await dashboard.create()
    if not created_dashboard:
        raise HTTPException(status_code=400, detail="Can not create dashboard")
    user = await User.get(user_id)
    update_query = {
        "$push": {
            'dashboards': PydanticObjectId(created_dashboard.id)
        }}
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Can not find user"
        )
    await user.update(update_query)
    return created_dashboard


async def delete_dashboard(
        dashboard_id: PydanticObjectId,
        user_id: PydanticObjectId
) -> Dashboard:
    """
    EN:

    RU:
    """
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find dashboard")
    await dashboard.delete()
    user = await User.get(user_id)
    update_query = {"$pull": {
        'dashboards': PydanticObjectId(dashboard.id)
    }}
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Can not find user"
        )
    await user.update(update_query)
    return dashboard
