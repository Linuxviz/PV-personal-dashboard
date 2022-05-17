import jwt
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from starlette.requests import Request

from auth.business.jwt_handler import secret_key
from dashboard.database.database import create_dashboard
from dashboard.models.dasboard import Dashboard, DashboardCreate, DashboardCreateResponse
from auth.business.jwt_bearer import JWTBearer

dashboards_router = APIRouter()


@dashboards_router.get("/{dashboard_id}", tags=['dashboards', ], response_model=Dashboard)
async def tag(dashboard_id: PydanticObjectId):
    """
    EN:
    RU: Возвращает данные дашборда по его id
    """
    # new_student = await collection_lo["students"].insert_one({'boba':tag_id})
    # created_student = await collection_lo["students"].find_one({"_id": new_student.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
    return {"message": f"Данные о Доске "}  # created_student


@dashboards_router.post("/", tags=['dashboards', ], response_model=DashboardCreateResponse)
async def tag(dashboard: DashboardCreate, credentials=Depends(JWTBearer())):
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
