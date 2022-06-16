from fastapi import FastAPI

from auth.business.jwt_bearer import JWTBearer
from auth.views import router as auth_router
from config.config import DataBase, db
from dashboard.routers.routers import versioned_router

description = """
PV Personal dashboard helps you manage you task and issues like as you want. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""
# TODO update desc
app = FastAPI(
    title='PV Personal dashboard',
    description=description,
    version='0.1',
    contact={
        'name': 'Victor Ivanov, ',
        'contact': "***",
        'email': 'some@mail.com',
    },
    license_info={
        'name': 'MIT',
    },
)

token_listener = JWTBearer()


@app.on_event('startup')
async def start_database():
    await db.initiate_database()


@app.on_event('shutdown')
async def out_database():
    await db.close_database()


@app.get("/", tags=['Main page'])
async def read_root():
    return {"message": "Welcome to this fantastic app.!!ff!!@"}


app.include_router(auth_router, tags=["Login"], prefix="/admin")
app.include_router(versioned_router)
