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
from beanie import PydanticObjectId

from dashboard.models.dasboard import Dashboard
from dashboard.models.tags import Tag


async def add_tag(dashboard_id: PydanticObjectId, tag: Tag) -> Tag:
    #FIXME the raw query may be more useful
    dashboard = await Dashboard.get(dashboard_id)
    update_query = {"$push": {
        'tags': tag
    }}

    if dashboard:
        created_tag = await dashboard.update(update_query)
        return created_tag
    return None
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