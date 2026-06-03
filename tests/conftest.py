"""
Pytest configuration and fixtures for the API tests.

This module provides shared fixtures for testing the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI application.
    
    Returns:
        TestClient: A test client for making requests to the API.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture to reset the activities dictionary before each test.
    
    This ensures that test state doesn't pollute other tests by
    resetting the in-memory activities database to a known state
    before each test execution.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team-based soccer training and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["ava@mergington.edu", "liam@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice shooting, dribbling, and team play",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["isabella@mergington.edu", "sophia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, improv, and theater production workshops",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["olivia@mergington.edu", "ethan@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Prepare for math competitions and solve challenging problems",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["jack@mergington.edu", "emma@mergington.edu"]
        },
        "Robotics Workshop": {
            "description": "Build robots and learn about engineering principles",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 14,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        }
    }
    
    # Clear and restore to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (restore to original state)
    activities.clear()
    activities.update(original_activities)
