import datetime
import uuid
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from config.config import db as mongodb
from dashboard.models.dashboard import Dashboard
from dashboard.schemas.columns import Column, ColumnCreate, ColumnUpdate
from dashboard.schemas.issues import IssueCreate, Issue, IssueUpdate, UpdateColumnInIssueData, AddTagInIssueData


async def get_issues(dashboard_id: PydanticObjectId) -> List[Column]:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {
        'issues': 1, '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues']


async def try_to_create_issue(dashboard_id: PydanticObjectId, issue: IssueCreate, collection):
    # TODO create back type
    is_created: bool = False
    id = uuid.uuid4()
    new_issue = Issue(
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        # creator: PydanticObjectId,
        # executor: PydanticObjectId,
        **issue.dict(),
        id=id
    )
    find_query = {
        "_id": dashboard_id,
        "issues.id": {"$ne": id},
        "issues.name": {"$ne": issue.name},
        "columns.id": new_issue.column_id
    }
    if new_issue.tags_ids:
        find_query["tags.id"] = {"$in": new_issue.tags_ids}
    update_query = {
        '$push': {'issues': new_issue.dict()}
    }
    result = await collection.update_one(find_query, update_query)
    if result.modified_count == 1:
        is_created = True
    return {'status': is_created, 'new_issue': new_issue}


async def create_issue(dashboard_id: PydanticObjectId, issue: IssueCreate) -> Issue:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    new_issue = None
    for _ in range(3):
        result = await try_to_create_issue(dashboard_id, issue, collection)
        if result['status']:
            new_issue = result['new_issue']
            break
    if not new_issue:
        raise HTTPException(status_code=400, detail=f'Can not create issue with this data: {issue}')
    return new_issue


async def get_issue(dashboard_id: PydanticObjectId, issue_id: uuid.UUID) -> Issue:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id,
    }
    projection_query = {
        "issues.$": 1
    }
    result = await collection.find_one(find_query, projection_query)
    if result:
        return result['issues'][0]


async def update_issue(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, issue: IssueUpdate) -> Issue:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    update_query = {}
    fields = issue.dict()
    for field in fields:
        if fields[field] is not None:
            update_query[f'issues.$.{field}'] = f'{fields[field]}'
            if field == 'name':
                find_query[f'issues.{field}'] = {"$ne": f'{fields[field]}'}
    result = await collection.update_one(
        find_query,
        {'$set': update_query}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="Check uniq of the name")
    result = await collection.find_one({"_id": dashboard_id}, {'_id': 0, 'issues': {'$elemMatch': {'id': issue_id}}})
    return Issue(**result['issues'][0])


async def delete_issue(dashboard_id: PydanticObjectId, issue_id: uuid.UUID) -> List[Column]:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    result = await collection.update_one(
        find_query,
        {'$pull': {'issues': {'id': issue_id}}}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    result = await collection.find_one({"_id": dashboard_id}, {'issues': 1, '_id': 0})
    return result['issues']


async def get_data_for_update_column_in_issue(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID
) -> UpdateColumnInIssueData:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {
        "issues": {"elemMatch": {'id': issue_id}, 'column_id': 1},
        "columns": 1,
    }
    try:
        result = await collection.find_one(find_query, projection_query)
    except:
        # TODO get logger
        pass
    columns_ids = [column['id'] for column in result['columns']]
    column_id = result['issues'][0]['column_id']
    return UpdateColumnInIssueData(columns_ids=columns_ids, column_id=column_id)


async def change_column_for_issue(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, column_id: uuid.UUID):
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    update_query = {'issues.$.column_id': column_id}
    result = await collection.update_one(
        find_query,
        {'$set': update_query}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    projection_query = {
        'issues': 1,
        '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues'][0]


async def get_issue_tags(dashboard_id: PydanticObjectId, issue_id: uuid.UUID) -> List[uuid.UUID]:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    projection_query = {
        "issues": {"elemMatch": {'id': issue_id}, 'tags_ids': 1},
    }
    result = await collection.find_one(
        find_query,
        projection_query
    )
    return result['issues'][0]['tags_ids']


async def get_data_for_add_tag_in_issue(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
) -> AddTagInIssueData:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {
        "issues": {"elemMatch": {'id': issue_id}, 'tags_ids': 1},
        "tags": 1,
    }
    result = await collection.find_one(find_query, projection_query)
    tags_ids_in_dashboard = [tag['id'] for tag in result['tags']]
    tags_ids_in_issue = result['issues'][0]['tags_ids']
    return AddTagInIssueData(
        tags_ids_in_issue=tags_ids_in_issue,
        tags_ids_in_dashboard=tags_ids_in_dashboard
    )


async def add_tag_for_issue(dashboard_id: PydanticObjectId, issue_id: uuid.UUID, tag_id: uuid.UUID):
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    update_query = {'issues.$.tags_ids': tag_id}
    result = await collection.update_one(
        find_query,
        {'$push': update_query}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    projection_query = {
        'issues': 1,
        '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues'][0]


async def get_data_for_pop_tag_from_issue(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
) -> List[uuid.UUID]:
    collection = await mongodb.get_collection('mongodb', 'dashboard')
    find_query = {
        "_id": dashboard_id,
    }
    projection_query = {
        "issues": {"elemMatch": {'id': issue_id}, 'tags_ids': 1},
    }
    result = await collection.find_one(find_query, projection_query)
    tags_ids_in_issue = result['issues'][0]['tags_ids']
    return tags_ids_in_issue


async def pop_tag_from_issue(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        tag_id: uuid.UUID
) -> Issue:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id
    }
    result = await collection.update_one(
        find_query,
        {'$pull': {'issues.$.tags_ids': tag_id}}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    projection_query = {
        'issues': 1,
        '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues'][0]


async def update_issue_name(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        name: str
) -> Issue:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id,
        "issues.name": {"$ne": name},
    }
    result = await collection.update_one(
        find_query,
        {'$set': {'issues.$.name': name}}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id,
    }
    projection_query = {
        'issues': 1,
        '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues'][0]


async def update_issue_description(
        dashboard_id: PydanticObjectId,
        issue_id: uuid.UUID,
        description: str
) -> Issue:
    db = await mongodb.get_db('mongodb')
    collection = db['dashboard']
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id,
    }
    result = await collection.update_one(
        find_query,
        {'$set': {'issues.$.description': description}}
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=400, detail="something wrong")
    find_query = {
        "_id": dashboard_id,
        "issues.id": issue_id,
    }
    projection_query = {
        'issues': 1,
        '_id': 0
    }
    result = await collection.find_one(find_query, projection_query)
    return result['issues'][0]
