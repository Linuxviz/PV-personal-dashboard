import jwt
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from starlette.requests import Request

from auth.business.jwt_handler import secret_key
from dashboard.database.database import create_dashboard, get_dashboard, get_dashboards
from dashboard.models.dasboard import Dashboard, DashboardCreate, DashboardCreateResponse, DashboardListResponse
from auth.business.jwt_bearer import JWTBearer

dashboards_router = APIRouter()


@dashboards_router.get("/dashboards", tags=['dashboards', ], response_model=DashboardListResponse)
async def get_dashboards_view(credentials=Depends(JWTBearer())):
    """
    EN:
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
        "status_code": 400,
        "response_type": "error",
        "description": f"Can not find dashboard with {credentials['user_id']} user",
    }

@dashboards_router.get("/{dashboard_id}", tags=['dashboards', ], response_model=DashboardCreateResponse)
async def get_dashboard_view(dashboard_id: PydanticObjectId):
    """
    EN:
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
    EN: Create dashboard, may be with background image
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
