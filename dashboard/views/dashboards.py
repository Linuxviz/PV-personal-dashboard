from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException

from auth.schemas import DashboardsIds
from dashboard.database.dashboards import get_dashboard, get_dashboards, create_dashboard, delete_dashboard
from dashboard.models.dashboard import Dashboard
from dashboard.schemas.dashboards import DashboardCreate
from auth.business.jwt_bearer import JWTBearer

dashboards_router = APIRouter()


@dashboards_router.get(
    "/dashboards",
    tags=['Dashboards', ],
    response_model=DashboardsIds
)
async def get_dashboard_objects_available_to_the_user(
        credentials=Depends(JWTBearer())
) -> DashboardsIds:
    """
    EN: Return **dict|object** of **lists** of dashboard ids grouped by status current user in itself

    RU: Возвращает **словарь|объект** списков с id дашбордов сгруппированных по статусу пользователя в них.
    """

    dashboards = await get_dashboards(credentials['user_id'])
    if dashboards:
        return dashboards
    raise HTTPException(
        status_code=400,
        detail=f"Can not find dashboards data for user id: {credentials['user_id']}."
    )


@dashboards_router.get(
    "/dashboard/{dashboard_id}",
    tags=['Dashboards', ],
    response_model=Dashboard
)
async def get_dashboard_object(
        dashboard_id: PydanticObjectId,
        credentials=Depends(JWTBearer())
) -> Dashboard:
    """
    EN: Return Dashboard data for id

    RU: Возвращает данные дашборда по его id
    """

    dashboard = await get_dashboard(dashboard_id)
    if dashboard:
        return dashboard
    raise HTTPException(
        status_code=400,
        detail=f"Can not find dashboard, check id."
    )


@dashboards_router.post(
    "/dashboard",
    tags=['Dashboards', ],
    response_model=Dashboard
)
async def create_dashboard_object(
        dashboard: DashboardCreate,
        credentials=Depends(JWTBearer())
):
    """
    EN: Create dashboard object

    RU: Создает дашборд
    """
    created_dashboard = await create_dashboard(dashboard, credentials['user_id'])
    if created_dashboard:
        return created_dashboard
    raise HTTPException(status_code=400, detail="Dashboard created unsuccessfully")


@dashboards_router.delete(
    "/dashboard/{dashboard_id}",
    tags=['Dashboards', ]
)
async def delete_dashboard_object(
        dashboard_id: PydanticObjectId,
        credentials=Depends(JWTBearer())
):
    """
    EN: REAL Delete dashboard

    RU: Удаляет дашборд, данные не помечаются как удаленные а действительно удаляются
    """
    # TODO разделить владельцев дашбордов и просто участников и настроить права доступа
    deleted_dashboard = await delete_dashboard(dashboard_id)
    if deleted_dashboard:
        return {"status": 'deleted', "dashboard_id": dashboard_id}
    raise HTTPException(status_code=400, detail="Dashboard delete unsuccessfully")
