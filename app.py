from fastapi import FastAPI, Depends

from auth.business.jwt_bearer import JWTBearer
# from routes.student import router as StudentRouter
from auth.views import router as auth_router
from config.config import initiate_database
from dashboard.routers.routers import versioned_router

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


# @app.on_event("shutdown")
# async def out_database():
#     await close_database()

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app.!!ff!!@"}


app.include_router(auth_router, tags=["Administrator"], prefix="/admin")
app.include_router(versioned_router)  #
