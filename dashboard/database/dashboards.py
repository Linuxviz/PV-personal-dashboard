from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException
from pymongo import UpdateMany

from auth.models import User
from auth.schemas import DashboardsIds
from dashboard.models.dashboard import Dashboard
from dashboard.schemas.dashboards import DashboardCreate, UsersIds
from config.config import db as mongodb


async def get_dashboard(dashboard_id: PydanticObjectId) -> Dashboard:
    """
    EN: Return Dashboard

    RU:
    """
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find dashboard")
    return dashboard


async def get_dashboards(user_id: PydanticObjectId) -> DashboardsIds:
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
    users_dict = UsersIds(owner_id=user_id)
    dashboard = Dashboard(**dashboard_data.dict(), users=users_dict)
    created_dashboard = await dashboard.create()
    if not created_dashboard:
        raise HTTPException(status_code=400, detail="Can not create dashboard")
    user = await User.get(user_id)
    update_query = {
        "$push": {
            'dashboards.owner_dashboards_ids': PydanticObjectId(created_dashboard.id)
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
):
    """
    EN:

    RU:
    """
    db = await mongodb.get_db('mongodb')
    dashboard_collection = db['dashboard']
    user_collection = db['user']
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {"users": 1}
    dashboard_users = await dashboard_collection.find_one(find_query, projection_query)
    if not dashboard_users:
        raise HTTPException(status_code=400, detail="Can not find dashboard")
    result = await user_collection.bulk_write([
        UpdateMany(
            filter={"_id": dashboard_users['users']['owner_id']},
            update={"$pull": {
                "dashboards.owner_dashboards_ids": dashboard_id
            }}
        ),
        UpdateMany(
            filter={"_id": {"$in": dashboard_users['users']['member_ids']}},
            update={"$pull": {
                "dashboards.member_dashboards_ids": dashboard_id
            }}
        ),
        UpdateMany(
            filter={"_id": {"$in": dashboard_users['users']['observer_ids']}},
            update={"$pull": {
                "dashboards.observer_dashboards_ids": dashboard_id
            }}
        ),
    ])
    # FIXME надо решить что возвращать
    result = await dashboard_collection.delete_one(filter={"_id": dashboard_id})
    if result:
        return True
