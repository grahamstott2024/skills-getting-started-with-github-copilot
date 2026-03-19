"""
Pytest AAA-style API tests for FastAPI app.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities

INITIAL_ACTIVITIES = deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))

@pytest.fixture
def client():
    return TestClient(app)

def test_get_activities_success(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()

def test_signup_and_refresh(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity_name = "Chess Club"
    # Act
    r1 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert r1.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

def test_remove_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    r2 = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    # Assert
    assert r2.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
