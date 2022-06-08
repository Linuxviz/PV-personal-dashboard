from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

#
# def test_update_issue():
#     response = client.get("pvd/v1/dashboard/{dashboard_id}/issue/{issue_id}/column/{column_id}")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
