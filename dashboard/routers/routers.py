from fastapi import APIRouter

# from dashboard.views.backgrounds import backgrounds_router
# from dashboard.views.colums import columns_router
# from dashboard.views.comments import comments_router
from dashboard.views.dashboard import dashboards_router
# from dashboard.views.issues import issues_router
from dashboard.views.tags import tags_router

dashboard_router = APIRouter(prefix="/dashboard")  # router for main objects on personal dashboard
dashboard_router.include_router(dashboards_router)
# dashboard_router.include_router(issues_router)
# dashboard_router.include_router(comments_router)
dashboard_router.include_router(tags_router)
# dashboard_router.include_router(backgrounds_router)
# dashboard_router.include_router(columns_router)

versioned_router = APIRouter(prefix="/v1")  # version api in router
versioned_router.include_router(dashboard_router)


# from fastapi import APIRouter, Body
#
# from database.database import *
# from models.student import *
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
# router = APIRouter()
#
#
# @router.get("/", response_description="Students retrieved", response_model=Response)
# async def get_students():
#     students = await retrieve_students()
#     return {
#         "status_code": 200,
#         "response_type": "success",
#         "description": "Students data retrieved successfully",
#         "data": students
#     }