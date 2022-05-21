from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from dashboard.database.dashboards import get_dashboard, get_dashboards, create_dashboard, delete_dashboard
from dashboard.schemas.dashboards import DashboardCreate, DashboardCreateResponse, DashboardListResponse
from auth.business.jwt_bearer import JWTBearer

dashboards_router = APIRouter()


@dashboards_router.get("/dashboards", tags=['dashboards', ], response_model=DashboardListResponse)
async def get_dashboards_view(credentials=Depends(JWTBearer())):
    """
    EN: Return list of dasboards id for current user

    RU: Возвращает список id дашбордов доступных пользователю
    """
    dashboards = await get_dashboards(credentials['user_id'])
    if dashboards:
        return {
            "dashboards_ids": dashboards,
            "status_code": 200,
            "response_type": "success",
            "description": "The list of ids dashboards for current user",
        }
    return {
        "dashboards_ids": [],
        "status_code": 400,
        "response_type": "error",
        "description": f"Can not find dashboard with {credentials['user_id']} user",
    }


@dashboards_router.get("/dashboard/{dashboard_id}", tags=['dashboards', ], response_model=DashboardCreateResponse)
async def get_dashboard_view(dashboard_id: PydanticObjectId, credentials=Depends(JWTBearer())):
    """
    EN: Return Dashboard data for id

    RU: Возвращает данные дашборда по его id
    """
    dashboard = await get_dashboard(dashboard_id)
    if dashboard:
        return {
            "dashboard": dashboard,
            "status_code": 200,
            "response_type": "success",
            "description": "Dashboard created successfully",
        }
    return {
        "dashboard": dashboard,
        "status_code": 400,
        "response_type": "error",
        "description": "Dashboard created unsuccessfully",
    }


@dashboards_router.post("/dashboard", tags=['dashboards', ], response_model=DashboardCreateResponse)
async def create_dashboard_view(dashboard: DashboardCreate, credentials=Depends(JWTBearer())):
    """
    EN: Create dashboard

    RU: Создает дашборд
    """
    created_dashboard = await create_dashboard(dashboard, credentials['user_id'])
    if created_dashboard:
        return {
            "dashboard": created_dashboard,
            "status_code": 200,
            "response_type": "success",
            "description": "Dashboard created successfully",
        }
    return {
        "dashboard": dashboard,
        "status_code": 400,
        "response_type": "error",
        "description": "Dashboard created unsuccessfully",
    }


@dashboards_router.delete("/dashboard/{dashboard_id}", tags=['dashboards', ], response_model=DashboardCreateResponse)
async def delete_dashboard_view(dashboard_id: PydanticObjectId, credentials=Depends(JWTBearer())):
    """
    EN: REAL Delete dashboard

    RU: Удаляет дашбордdelete
    """
    # TODO разделить владельцев дашбордов и просто участников и настроить права доступа
    deleted_dashboard = await delete_dashboard(dashboard_id, credentials['user_id'])
    if deleted_dashboard:
        return {
            "dashboard": deleted_dashboard,
            "status_code": 200,
            "response_type": "success",
            "description": "Dashboard delete successfully",
        }
    return {
        "dashboard": dashboard_id,
        "status_code": 400,
        "response_type": "error",
        "description": "Dashboard delete unsuccessfully",
    }
