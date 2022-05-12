# from fastapi import APIRouter, Body
#
# from database.database import *
# from models.student import *
#
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