import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 308)
    # Accepts redirect or direct serve

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())

def test_signup_and_duplicate():
    # Pick an activity
    response = client.get("/activities")
    activities = response.json()
    activity = next(iter(activities))
    email = "pytestuser@mergington.edu"
    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    # Duplicate signup should fail
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400
    assert "already signed up" in dup.json().get("detail", "")

def test_signup_missing_email():
    response = client.post("/activities/Basketball/signup")
    assert response.status_code == 422 or response.status_code == 400
