# examples
# database contains methods contains logic of connections to database


# from typing import List, Union
#
# from beanie import PydanticObjectId
#
# from models.admin import Admin
# from models.student import Student
#
# admin_collection = Admin
# student_collection = Student
#
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from auth.models import User
from dashboard.models.dasboard import Dashboard, DashboardCreate
from dashboard.models.tags import Tag


async def add_tag(dashboard_id: PydanticObjectId, tag: Tag) -> Tag:
    # FIXME the raw query may be more useful
    dashboard = await Dashboard.get(dashboard_id)
    update_query = {"$push": {
        'tags': tag
    }}

    if dashboard:
        created_tag = await dashboard.update(update_query)
        return created_tag
    return None


async def get_dashboard(dashboard_id: PydanticObjectId) -> Dashboard:
    """
    EN: Return Dashboard

    RU:
    """
    dashboard = await Dashboard.get(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=400, detail="Can not find dashboard")
    return dashboard


async def get_dashboards(user_id: PydanticObjectId) -> List[PydanticObjectId]:
    """
    EN: Return list of ids dashboards current user

    RU:
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Can not find user")
    return user.dashboards


async def create_dashboard(dashboard_data: DashboardCreate, user_id: PydanticObjectId) -> Dashboard:
    """
    EN: When we create dashboard we should add dashboard to user model

    RU:
    """
    dashboard = Dashboard(**dashboard_data.dict())
    created_dashboard = await dashboard.create()
    if not created_dashboard:
        raise HTTPException(status_code=400, detail="Can not create dashboard")
    user = await User.get(user_id)
    update_query = {"$push": {
        'dashboards': PydanticObjectId(created_dashboard.id)
    }}
    if not user:
        raise HTTPException(status_code=400, detail="Can not find user")
    await user.update(update_query)
    return created_dashboard

#
#
# async def retrieve_students() -> List[Student]:
#     students = await student_collection.all().to_list()
#     return students
#
#
# async def add_student(new_student: Student) -> Student:
#     student = await new_student.create()
#     return student
#
#
# async def retrieve_student(id: PydanticObjectId) -> Student:
#     student = await student_collection.get(id)
#     if student:
#         return student
#
#
# async def delete_student(id: PydanticObjectId) -> bool:
#     student = await student_collection.get(id)
#     if student:
#         await student.delete()
#         return True
#
#
# async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
#     des_body = {k: v for k, v in data.items() if v is not None}
#     update_query = {"$set": {
#         field: value for field, value in des_body.items()
#     }}
#     student = await student_collection.get(id)
#     if student:
#         await student.update(update_query)
#         return student
#     return False
