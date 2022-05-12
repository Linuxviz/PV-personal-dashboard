from fastapi import FastAPI

from auth.business.jwt_bearer import JWTBearer
# from routes.student import router as StudentRouter
from auth.views import router as auth_router
from config.config import initiate_database

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app.!!ff!!@"}


app.include_router(auth_router, tags=["Administrator"], prefix="/admin")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
