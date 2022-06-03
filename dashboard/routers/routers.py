from fastapi import APIRouter, Depends

from auth.business.jwt_bearer import JWTBearer
from dashboard.views.columns import columns_router
from dashboard.views.dashboard import dashboards_router
from dashboard.views.issue import issues_router
from dashboard.views.tags import tags_router

dashboard_router = APIRouter(prefix="/pvd")  # router for main objects on personal dashboard
dashboard_router.include_router(dashboards_router)
dashboard_router.include_router(issues_router)
# dashboard_router.include_router(comments_router)
dashboard_router.include_router(tags_router)
# dashboard_router.include_router(backgrounds_router)
dashboard_router.include_router(columns_router)

versioned_router = APIRouter(prefix="/v1")  # version api in router
versioned_router.include_router(dashboard_router)
